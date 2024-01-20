# SimpleCmdScan - A simple command line scanning tool
# Copyright (C) 2024, bitcreed LLC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import locale
import os
import tempfile
from pypdf import PdfWriter, PdfReader
from PIL import Image
import io
import sane

from datetime import datetime
from .logger import log


class ScanJob:
    def __init__(self, default_complete=False) -> None:
        self.scanned_page_images = []
        self.complete = default_complete

    @property
    def images(self):
        return self.scanned_page_images

    @property
    def num_pages(self):
        return len(self.scanned_page_images)

    def add_image(self, im):
        self.scanned_page_images.append(im)

    def mark_complete(self, complete=True):
        self.complete = complete

    def merge_back_images(self, scan_back):
        if self.num_pages != scan_back.num_pages:
            raise ValueError("Number of front and back pages needs to be the same")

        combined = ScanJob(default_complete=True)
        combined.scanned_page_images = [None] * (self.num_pages + scan_back.num_pages)
        combined.scanned_page_images[::2] = self.images
        combined.scanned_page_images[1::2] = scan_back.images[::-1]
        return combined

    def create_pdf(self, output_dir, output_filename=None, suffix=""):
        if not self.scanned_page_images:
            log.debug("No scans available, not creating PDF")
            return

        pdf_writer = PdfWriter()

        for path in self.scanned_page_images:
            image = Image.open(path)
            if image.mode == "RGBA":
                image = image.convert("RGB")

            pdf_bytes = io.BytesIO()
            image.save(pdf_bytes, format="PDF")
            pdf_writer.append_pages_from_reader(PdfReader(pdf_bytes))

        output_filename = output_filename or f"{datetime.now().strftime('%Y-%m-%d_%H%M')}_scan{suffix}.pdf"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "wb") as f:
            pdf_writer.write(f)

        log.info(f"PDF created: {output_path}")


class SimpleCmdScan:
    MAX_SCANS = 10000  # To avoid infinite loops, set a max number of documents in ADF and single consecutive scans
    RET_OK = 0
    RET_ERR = 1
    RET_NO_SCANNER = 2
    DEFAULT_RESOLUTION_TEXT = 150
    DEFAULT_RESOLUTION_PICTURE = 300
    # Common paper sizes in mm (width x height)
    PAPER_SIZES_MM = {
        'a4': (210, 297),
        'letter': (215.9, 279.4),
        'legal': (215.9, 355.6)
    }

    def __init__(self, args):
        self.scanner = None
        self.find_scanners = args.find_scanners
        self.scan_device = args.scanner
        self.output_dir = args.output_dir or os.getcwd()
        self.adf_scan = args.adf
        self.paper_format = args.paper_format
        self.resolution_dpi = args.resolution_dpi or SimpleCmdScan.DEFAULT_RESOLUTION_TEXT
        self.double_sided = args.double_sided
        self.multidoc_mode = args.multidoc
        # Initialize SANE
        try:
            sane.init()
        except Exception as e:
            log.error(f"Error initializing SANE: {e}")

    @staticmethod
    def get_default_paper_size():
        # Check LC_PAPER environment variable
        loc = os.environ.get('LC_PAPER')
        loc = loc and loc.split('.') or loc
        if not loc:
            # Fallback: Check locale settings
            loc = locale.getlocale()

        if loc[0] and ('US' in loc[0] or 'CA' in loc[0]):
            return 'letter'
        return 'a4'  # Most other countries use A4

    def set_paper_size(self, paper_format=None):
        paper_format = paper_format and paper_format.lower() or SimpleCmdScan.get_default_paper_size()
        if paper_format not in SimpleCmdScan.PAPER_SIZES_MM:
            def_paper_format = SimpleCmdScan.get_default_paper_size()
            if paper_format:
                log.error(f"Unsupported paper format: {paper_format}. Using default {def_paper_format}.")
            paper_format = def_paper_format
        log.debug(f"Using paper format {paper_format}")

        width_mm, height_mm = SimpleCmdScan.PAPER_SIZES_MM[paper_format]

        # self.scanner.unit = "UNIT_MM"
        self.scanner.br_x = width_mm
        self.scanner.br_y = height_mm

    def list_scanners(self):
        # Format:
        # [('escl:http://192.168.1.40:8080', 'HP', 'ENVY 7640 series [DCE7DB]', 'platen,adf scanner'),
        #  ('hpaio:/net/ENVY_7640_series?ip=192.168.1.23', 'Hewlett-Packard', 'ENVY_7640_series', 'all-in-one'),
        #  ('hpaio:/net/envy_7640_series?ip=192.168.1.40&queue=false', 'Hewlett-Packard', 'envy_7640_series', 'all-in-one'),
        #  ('airscan:e0:HP ENVY 7640 series [DCE7DB]', 'eSCL', 'HP ENVY 7640 series [DCE7DB]', 'ip=192.168.1.40')]
        log.debug("Finding scanners...")
        devices = sane.get_devices()
        log.debug(f"Available scanning devices: {devices}")
        return devices

    def open_scanner(self):
        try:
            scanner = self.scan_device
            if not scanner:
                devices = self.list_scanners()
                if not devices:
                    log.warning("No scanners found.")
                    return SimpleCmdScan.RET_NO_SCANNER
                # Use the first available scanner
                scanner = devices[0][0]

            log.info(f"Using device {scanner}")
            self.scanner = sane.open(scanner)
            self.scanner.resolution = self.resolution_dpi
            self.set_paper_size(self.paper_format)
            if self.adf_scan:
                log.debug("Configuring scanner for ADF...")
                self.scanner.source = "ADF"
                self.scanner.batch_scan = True

        except Exception as e:
            log.error(f"Error opening scanner: {e}")
            return SimpleCmdScan.RET_ERR

        return SimpleCmdScan.RET_OK

    def close_scanner(self):
        if self.scanner:
            self.scanner.close()
            self.scanner = None
        sane.exit()

    @staticmethod
    def _save_single_page(im, idx, temp_dir):
        file_name = f"scan_{idx}.png"
        file_path = os.path.join(temp_dir, file_name)
        im.save(file_path)
        log.debug(f"Scanned image saved to {file_path}")
        return file_path

    def _handle_sane_error(e, job):
        job.mark_complete(False)
        if str(e) == "Document feeder jammed":
            log.error(e)
        else:
            log.exception(f"An error occurred during scanning: {e}")

    def _run_one_sided_scan(self, temp_dir, idx_offset=0, job=None):
        if self.adf_scan:
            return self._run_multi_scan(temp_dir, idx_offset)

        try:
            log.debug("Scanning page...")
            job = job or ScanJob(default_complete=True)
            im = self.scanner.scan()
            file_path = SimpleCmdScan._save_single_page(im, job.num_pages + idx_offset + 1, temp_dir)
            job.add_image(file_path)

        except sane.error as e:
            self._handle_sane_error(e, job)

        except Exception as e:
            job.mark_complete(False)
            log.exception(f"An error occurred during scanning: {e}")

        return job

    def _run_multi_scan(self, temp_dir, idx_offset=0):
        job = ScanJob()
        try:
            for i, im in enumerate(self.scanner.multi_scan()):
                file_path = SimpleCmdScan._save_single_page(im, idx_offset + i, temp_dir)
                job.add_image(file_path)
            job.mark_complete()

        except sane.error as e:
            self._handle_sane_error(e, job)

        except Exception as e:
            log.exception(f"An error occurred during scanning: {e}")

        return job

    def scan_single_sided(self):
        ret = self.open_scanner()
        if ret != SimpleCmdScan.RET_OK:
            return ret

        with tempfile.TemporaryDirectory(prefix="scan") as temp_dir:
            job = None
            if self.multidoc_mode in [None, "join"]:
                job = ScanJob(default_complete=True)

            try:
                for i in range(SimpleCmdScan.MAX_SCANS):
                    job = self._run_one_sided_scan(temp_dir, job=job)
                    if self.multidoc_mode is None:
                        break
                    else:
                        if self.multidoc_mode == "split":
                            job.create_pdf(self.output_dir)
                            job = None

                        input(
                            "Please feed the next document(s) and press Enter to continue or CTRL+D to stop..."
                        )

            except EOFError:
                # CTRL+D pressed
                pass

            finally:
                self.close_scanner()
                if job is not None:
                    job.create_pdf(self.output_dir)

        return SimpleCmdScan.RET_OK

    def scan_double_sided(self):
        ret = self.open_scanner()
        if ret != SimpleCmdScan.RET_OK:
            return ret

        with tempfile.TemporaryDirectory(prefix="simple_cmd_scan_") as temp_dir:
            try:
                # Scan the front sides
                scan_front = self._run_one_sided_scan(temp_dir)
                if not scan_front.complete:
                    log.error(
                        "Error while scanning, aborting double-sided scan. Saving partial scan."
                    )
                    scan_front.create_pdf(self.output_dir, "_front_partial")
                    return SimpleCmdScan.RET_ERR

                try:
                    input("Please flip the stack and press Enter to continue scanning the back sides or CTRL+D to abort...")

                except EOFError:
                    scan_front.create_pdf(self.output_dir, "_front")
                    return SimpleCmdScan.RET_ERR

                # Scan the back sides
                scan_back = self._run_one_sided_scan(temp_dir, scan_front.num_pages)
                if not scan_back.complete:
                    log.error(
                        "Error while scanning, aborting double-sided scan. Saving partial scans."
                    )
                    scan_front.create_pdf(self.output_dir, "_front")
                    scan_back.create_pdf(self.output_dir, "_back_partial")
                    return SimpleCmdScan.RET_ERR

            finally:
                self.close_scanner()

            if scan_front.num_pages != scan_back.num_pages:
                log.error(
                    "Mismatch in the number of front and back pages. Creating separate output files."
                )
                scan_front.create_pdf(self.output_dir, "_front")
                scan_back.create_pdf(self.output_dir, "_back")
                return SimpleCmdScan.RET_ERR

            # Reorder back images (as they are in reverse order)

            # Combine front and back images
            combined = scan_front.merge_back_images(scan_back)
            combined.create_pdf(self.output_dir)

        return SimpleCmdScan.RET_OK

    def run(self):
        if self.find_scanners:
            scanners = self.list_scanners()
            for s in scanners:
                print(f"Scanner: {s[0]}")
                print(f"  Model: {s[1]} {s[2]}")
            print()
            return (
                len(scanners) == 0
                and SimpleCmdScan.RET_NO_SCANNER
                or SimpleCmdScan.RET_OK
            )

        ret = SimpleCmdScan.RET_OK
        if self.double_sided:
            ret = self.scan_double_sided()
        else:
            ret = self.scan_single_sided()

        return ret
