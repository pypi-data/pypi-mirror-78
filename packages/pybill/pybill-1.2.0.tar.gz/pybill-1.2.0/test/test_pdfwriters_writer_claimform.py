# -*- coding: utf-8 -*-

from logilab.common.testlib import TestCase

from pybill.lib.pdfwriters import PDFWriter
from pybill.lib.entities.accounting_docs import ClaimForm

from generic_test_pdfwriter import PDFWriterGenericTest


class PDFWriterClaimFormTest(TestCase, PDFWriterGenericTest):
    def setUp(self):
        """
        Called before each test from this class.
        """
        self.writer = PDFWriter()
        self.acc_doc = ClaimForm("identifier")
        self.acc_doc.cfg_data = self._build_config_data()
        self._fill_acc_doc_metadata(self.acc_doc)
        self.acc_doc.sender = self._build_person_address(u"sd")
        self.acc_doc.receiver = self._build_person_address(u"rc")
        self.acc_doc.payment_terms = "payment_terms"
        self.entity_name = "claimform"


# definitions for automatic unit testing

if __name__ == "__main__":
    import unittest

    unittest.main()
