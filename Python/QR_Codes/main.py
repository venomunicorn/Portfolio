import sys

def main():
    print("--- QR Code Generator ---")
    
    try:
        import qrcode
    except ImportError:
        print("Error: 'qrcode' library not installed.")
        print("Falling back to Simulation Mode (ASCII Art placeholder).")
        print("To fix: pip install qrcode[pil]")
        print("\n[PREVIEW]")
        print("##############")
        print("#  ##  ##  #")
        print("#  ##  ##  #")
        print("##############")
        print("#  ##  ##  #")
        print("##############")
        return

    data = input("Enter text/URL to encode: ").strip()
    if not data:
        data = "https://example.com"
        print(f"No input provided. Defaulting to: {data}")

    # Generate QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Save
    filename = "result_qr.png"
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"Success! QR code saved to {filename}")

    # ASCII Display
    print("\nTerminal Preview:")
    qr.print_ascii()

if __name__ == "__main__":
    main()
