import argparse

def test(input_file, output_file):
    # Your main logic here
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A sample program that takes input and output file names.")
    parser.add_argument("--input", required=True, help="Input file name")
    parser.add_argument("--output", required=True, help="Output file name")

    args = parser.parse_args()
    test(args.input, args.output)
