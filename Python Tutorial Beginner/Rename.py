# Python 3 code to rename multiple
# files in a directory or folder 

# importing os module 
import os


# Function to rename multiple files 
def main():
    key = list(map(str, "3456789"))
    for count, filename in enumerate(os.listdir("C:\\Users\\pyjpa\\Desktop\\Python\\Python Tutorial Beginner")):
        dst = list(set([filename for i in key if i in filename and "1" not in filename]))
        src = filename
        if dst:
            dst = "0" + dst[0]
            print(dst)
            os.rename(src, dst)


# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()
