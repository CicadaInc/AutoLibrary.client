from BAR import BarcodeGenerator

bar = BarcodeGenerator('ean13')
bar.generate_barcode('1234567890112', 'test')
