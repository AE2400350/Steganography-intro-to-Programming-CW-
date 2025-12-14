import os

class Steganography:
    def __init__(self):
        self.delimiter = "###END###"
    
    def _text_to_binary(self, text):
        return ''.join(format(ord(c), '08b') for c in text + self.delimiter)
    
    def _binary_to_text(self, binary):
        text = ""
        for i in range(0, len(binary), 8):
            if i + 8 > len(binary): break
            text += chr(int(binary[i:i+8], 2))
            if text.endswith(self.delimiter):
                return text[:-len(self.delimiter)]
        return text
    
    def _read_ppm(self, path):
        with open(path, 'rb') as f:
            if f.readline().strip() != b'P6': raise ValueError("Only P6 PPM supported")
            w, h = map(int, f.readline().split())
            f.readline()  # Skip max color
            return w, h, list(f.read())
    
    def _write_ppm(self, path, w, h, pixels):
        with open(path, 'wb') as f:
            f.write(b'P6\n' + f"{w} {h}\n".encode() + b'255\n' + bytes(pixels))
    
    def hide(self, input_path, output_path, text):
        w, h, pixels = self._read_ppm(input_path)
        binary = self._text_to_binary(text)
        
        if len(binary) > len(pixels):
            raise ValueError("Image too small")
        
        for i in range(len(binary)):
            pixels[i] = (pixels[i] & 0xFE) | int(binary[i])
        
        self._write_ppm(output_path, w, h, pixels)
        print(f"Hidden in {output_path}")
    
    def extract(self, image_path):
        w, h, pixels = self._read_ppm(image_path)
        binary = ''.join(str(p & 1) for p in pixels)
        return self._binary_to_text(binary)

def create_sample_image(path="sample.ppm", size=100):
    with open(path, 'wb') as f:
        f.write(b'P6\n' + f"{size} {size}\n".encode() + b'255\n')
        for y in range(size):
            for x in range(size):
                f.write(bytes([x%256, y%256, (x+y)%256]))
    print(f"Created {path}")

def main():
    stego = Steganography()
    
    if not os.path.exists("sample.ppm"):
        create_sample_image()
    
    print("1.Hide 2.Extract 3.Create image")
    choice = input("Choice: ")
    
    if choice == '1':
        stego.hide(
            input("Input image [sample.ppm]: ") or "sample.ppm",
            input("Output image [secret.ppm]: ") or "secret.ppm",
            input("Text to hide: ")
        )
    elif choice == '2':
        path = input("Image path: ")
        print(f"Extracted: {stego.extract(path)}")
    elif choice == '3':
        create_sample_image()
    else:
        print("Invalid")

if __name__ == "__main__":
    main()
