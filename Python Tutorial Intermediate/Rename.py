# Python 3 code to rename multiple
# files in a directory or folder 

# importing os module 
import os


# Function to rename multiple files 
def main():
    key = list(map(str, "123456789"))
    for count, filename in enumerate(os.listdir("C:\\Users\\pyjpa\\Desktop\\Python\\Python Tutorial Intermediate")):
        dst = list(set([filename[-5:-3] for i in key if i in filename]))
        src = filename
        if dst:
            dst = f"{dst[0]}_{filename[0].upper()}{filename[1:-6]}.py"
            print(dst)
            os.rename(src, dst)


# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()
