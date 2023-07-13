import os
import heapq

class Huffmanzipper:
    def __init__(self,file_path):
        self.file_path=file_path
        self.heap=[]
        self.encodeDict={}
        self.decodeDict={}

    class Node:
        def __init__(self,char,freq):
            self.char=char
            self.freq=freq
            self.left=None
            self.right=None

        def __lt__(self, other):
            return self.freq< other.freq

        def __eq__(self, other):
            if other==None:
                return False
            return self.value == other.value

    #Encoding

    def get_frequency(self,data):

        frequency={}
        for char in data:
            if char not in frequency:
                frequency[char]=0
            frequency[char]+=1
        return frequency

    def add_in_heap(self,frequency):

        for char in frequency:
            node=self.Node(char,frequency[char])
            heapq.heappush(self.heap,node)

    def make_tree(self):
        while(len(self.heap)>1):
            left = heapq.heappop(self.heap)
            right = heapq.heappop(self.heap)

            new_node = self.Node(None, left.freq + right.freq)
            new_node.left = left
            new_node.right = right

            heapq.heappush(self.heap,new_node)

    def traverse(self,curr_code,root_node):
        if root_node==None:
            return
        if root_node.char!=None:
            self.encodeDict[root_node.char]=curr_code
            self.decodeDict[curr_code]=root_node.char
            return

        self.traverse(curr_code+"0",root_node.left)
        self.traverse(curr_code+"1",root_node.right)


    def get_encode_dict(self):
        curr_code=""
        root_node=heapq.heappop(self.heap)
        self.traverse(curr_code,root_node)

    def get_encoded_data(self,data):
        encoded_data=""
        for char in data:
            encoded_data+=self.encodeDict[char]

        return encoded_data

    def padding_zeros(self,encode_data):
        zeros = 8 - len(encode_data) % 8
        # encode_data += zeros * "0" + format(zeros, "08b")

        for i in range(zeros):
            encode_data+="0"
        zero_info= "{0:08b}".format(zeros)
        encode_data = zero_info + encode_data

        return encode_data

    def conversion(self, paded_txt):
        b=bytearray()

        for i in range(0, len(paded_txt), 8):
            byte = paded_txt[i:i+8]
            b .append(int(byte, 2))

        return b

    def compress(self):
        filename, file_ext = os.path.splitext(self.file_path)
        output_file = filename + ".bin"

        with open(self.file_path, "r") as file, open(output_file,"wb") as output_data:
            data = file.read()
            data = data.rstrip()

            frequency = self.get_frequency(data)
            self.add_in_heap(frequency)
            self.make_tree()
            self.get_encode_dict()

            encode_data = self.get_encoded_data(data)

            paded_txt = self.padding_zeros(encode_data)
            b = self.conversion(paded_txt)

            output_data.write(b)

        return output_file

    #Decoding

    def remove_padding(self, bits_data):

        padding_info = bits_data[:8]
        extra_zero = int(padding_info, 2)
        bits_data = bits_data[8:]
        new_txt = bits_data[:-1*extra_zero]

        return new_txt

    def decoding(self,new_txt):
        decoded_txt = ""
        curr_bit = ""
        for bit in new_txt:
            curr_bit += bit
            if curr_bit in self.decodeDict:
                character = self.decodeDict[curr_bit]
                decoded_txt += character
                curr_bit = ""

        return decoded_txt



    def decompress(self,bin_file):
        filename,file_ext = os.path.splitext(self.file_path)
        output_file = filename + "_decoded" +".txt"

        with open(bin_file, "rb") as file, open(output_file, "w") as output_data:
            bits_data = ""
            byte = file.read(1)

            while len(byte)>0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bits_data += bits
                byte = file.read(1)

            new_txt = self.remove_padding(bits_data)

            decoded_txt = self.decoding(new_txt)

            output_data.write(decoded_txt)

        return output_file

path=str(input("Enter location of the txt file: "))

H = Huffmanzipper(path)
encoded=H.compress()
print("You can find your ENCODED file at: {}".format(encoded))
print("You can find your DECODED file at: {}".format(H.decompress(encoded)))


