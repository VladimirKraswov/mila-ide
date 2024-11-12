import esptool

def flash_firmware(port, firmware_path):
    esptool.main(['--port', port, 'write_flash', '0x1000', firmware_path])