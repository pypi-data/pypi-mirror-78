from pyground.timestamps import hoist_timestamp


def test_hoist_timestamp():
    # macOS Screenshot.app output
    assert (
        hoist_timestamp("Screen Shot 2020-01-02 at 03.45.01 PM.png")
        == "20200102T154501 Screen Shot.png"
    )
    # Dropbox's Camera Uploads
    assert hoist_timestamp("2020-02-03 04.50.12.jpg") == "20200203T045012.jpg"
    # download with time
    assert (
        hoist_timestamp("Invoice 2020-01-02 12-34 PM.pdf")
        == "20200102T1234 Invoice.pdf"
    )
    # download without time
    assert hoist_timestamp("20200101-OrderReceipt.pdf") == "20200101-OrderReceipt.pdf"
    # no timestamp at all
    assert hoist_timestamp("README.txt") == "README.txt"
