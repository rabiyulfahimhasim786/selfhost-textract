from app.extract import process_file


def test_sample_invoice():
    res = process_file('example_invoices/sample_invoice_1.png')
    assert 'pages' in res
    assert isinstance(res['pages'], list)