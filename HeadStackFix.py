#!/usr/bin/python3

from argparse import ArgumentParser
import os,sys,urllib.request,shutil


def Rebuild_File(hex,start,end):
     global File_Result

     print("\nFound %s at offset %d to %d "%(hex,start,end))
     print("\nFound %s at offset %d to %d "%(hex,start,end),file=Logging)
     print("Saving to File_Result...\n")
     print("Saving to File_Result...\n",file=Logging)
     if "." not in File_Result[start:end]:
           if File_Result[start:end-1] == hex[0] and File_Result[start+1:end] == hex[1]:
                 print("!!Strange coincidence!!\nFile already is containing %s at offset %d to %d"%(hex,start,end))
                 print("!!Strange coincidence!!\nFile already is containing %s at offset %d to %d"%(hex,start,end),file=Logging)
                 return
           if File_Result[start:end-1] != hex[0] and File_Result[start+1:end] != hex[1]:
                 File_Result[start:end] = hex
                 return
     File_Result[start:end] = hex
     return

def DotFilling(file):
     doted = []
     for i in range(Matching_Goal):
          doted.append(".")
     return doted

def LoadInput(Original_Sample_Name):
     if os.path.isfile(Original_Sample_Name) is True:
         with open(Original_Sample_Name, 'rb') as f:
             Original_Sample = f.read().hex()
     else:
         with urllib.request.urlopen(Source_Sample) as response, open(Original_Sample_Name, 'wb') as Sample_Out:
              shutil.copyfileobj(response, Sample_Out)
         with open(Original_Sample_Name, 'rb') as f:
              Original_Sample = f.read().hex()

     print("Setting Matching_Goal to :",len(Original_Sample))
     print("Setting Matching_Goal to :",len(Original_Sample),file=Logging)
     print("Origin_Data Loaded.\n")
     print("Origin_Data Loaded.\n",file=Logging)
     return(Original_Sample,len(Original_Sample))




def Similarity():
   global File_Result

   print("\nLooking for occurences inside all samples.")
   print("\nLooking for occurences inside all samples.",file=Logging)

   h = 0
   x = 2
   Total_Samples = len(os.listdir("./Samples/"))

   while True:

       if x <= Matching_Goal:
           Hex_Similarity=[]
           Match_Counter = 0
           Best_Match = ""
#           Samples_Counter = 0

           for filename in os.listdir("./Samples/"):

#                Samples_Counter = Samples_Counter+1

#                print("\nOpening :%s (%s/%s) at offset %s/%s"%(filename,Samples_Counter,Total_Samples,h,Matching_Goal))
#                print("\nOpening :%s at offset %s/%s"%(filename,h,Matching_Goal),file=Logging)

                with open("./Samples/"+filename,"rb") as s:
                    samples=s.read().hex()
                    Hex_Similarity.append(str(samples[h:x]))


           print("\nCounting how many occurences found at the same offset inside all samples.\n")
           print("\nCounting how many occurences found at the same offset inside all samples .\n",file=Logging)

           for match in Hex_Similarity:
                if Hex_Similarity.count(match) > Match_Counter:
                        Match_Counter = Hex_Similarity.count(match)
                        Best_Match = match

           print("\nSaving Best Match with %s Occurences %s to File_Result at offset :%s\n"%(Match_Counter,Best_Match,h))
           print("\nSaving Best Match with %s Occurences %s to File_Result at offset :%s\n"%(Match_Counter,Best_Match,h),file=Logging)

           File_Result[h:x] = Best_Match


           print("\nDone searching for occurences inside %s samples at Offset :%s"%(Total_Samples,h))
           print("\nDone searching for occurences inside %s samples at Offset :%s"%(Total_Samples,h),file=Logging)
           h = h+2
           x = x+2
       else:
           break





def SaveOutput(data):

     with open("Output.fix.hexadecimal", 'w') as f:
         f.write(data)
     print("Output.fix.hexadecimal as been saved .\n")
     print("Output.fix.hexadecimal as been saved .\n",file=Logging)

     with open("Output.fix.binary","wb") as f:
         f.write(bytes.fromhex(data))
     print("Output.fix.binary as been saved .\n")
     print("Output.fix.binary as been saved .\n",file=Logging)

def SaveSamples(data):

     filename = "./Samples/Sample."+str(Try)
     with open(filename, 'wb') as f:
         f.write(data)
     print("%s as been saved!!\n"%(filename))
#     print("%s as been saved .\n"%(filename),file=Logging))
     return

def GetNewSample(source):
       print("\nGetting new sample.")
       print("\nGetting new sample.",file=Logging)
       response = urllib.request.urlopen(source)
       data = response.read()
       SaveSamples(data)
       return(data)

def LenCheck(orig,new):
     if len(new) == len(orig):
        print("\nNumber of char in both sample are equal.")
        print("\nNumber of char in both sample are equal.",file=Logging)
        return(True)
     else:
        print("\nNumber of char in both sample are NOT equal.")
        print("\nNumber of char in both sample are NOT equal.",file=Logging)
        return(False)


def HexDiff(orig,new):
   print("\nLooking for occurences between in both samples.")
   print("\nLooking for occurences between in both samples.",file=Logging)
   h=0
   x=2
   while True:
       if orig[h:x] == new[h:x]:
          Rebuild_File(orig[h:x],h,x)
       h = h+2
       x = x+2
       if x >= Matching_Goal:
           break
   print("\nDone searching for occurences inside those samples.\n")
   print("\nDone searching for occurences inside those samples.\n",file=Logging)

def HexShaker(hex_sig,hex_sample):

     if hex_sig == hex_sample:
        return True

     hex_sig=int(hex_sig, 16)
     bin_sig=format(hex_sig,'b')

     for i in range(len(bin_sig)):

         Shaker=list(bin_sig)

         if Shaker[i] == "1":
              Shaker[i] = "0"
         else:
              Shaker[i] = "1"
         Shaker = int("".join(Shaker),2)
         Shaker = f'{Shaker:x}'
         if Shaker == hex_sample:
             print("Shaker %s and hexSample %s ARE equal !"%(Shaker,hex_sample))
             print("Shaker %s and hexSample %s ARE equal !"%(Shaker,hex_sample),file=Logging)
         else:
             print("Shaker %s and hexSample %s are NOT equal...."%(Shaker,hex_sample))
             print("Shaker %s and hexSample %s are NOT equal...."%(Shaker,hex_sample),file=Logging)

def SigSeeker(siglist,data_sample):

     print("Looking for File Signature...\n")
     print("Looking for File Signature...\n",file=Logging)

     for sig in siglist:

         start= 0
         end = 2

         sig_name = sig.split("**")[0]
         sig_hex = sig.split("**")[1].split(" ")

         Bingo = 0

         print("Trying to find %s signature...\n"%sig_name)
         print("Trying to find %s signature...\n"%sig_name,file=Logging)
         while True:
            print("Sample offset: %s/%s \n"%(start,Matching_Goal))
            print("Sample offset: %s/%s \n"%(start,Matching_Goal),file=Logging)
#
            if len(data_sample[start:end]) < 2:
                  break
#
            check=HexShaker(sig_hex[Bingo],data_sample[start:end])

            if check is True:

                     print("Found %s from %s %s at offset %s/%s ."%(sig_hex[Bingo],sig_name,sig_hex,start,Matching_Goal))
                     print("Found %s from %s %s at offset %s/%s ."%(sig_hex[Bingo],sig_name,sig_hex,start,Matching_Goal),file=Logging)
                     Bingo = Bingo + 1
                     print("Bingo power : %s/%s .."%(Bingo,len(sig_hex)))
                     print("Bingo power : %s/%s .."%(Bingo,len(sig_hex)),file=Logging)
                     if Bingo > 1:
                             pause = input("Bingo Alert")
            else:
                     Bingo = 0

            if Bingo == len(sig_hex):

                    print("/n!! Found %s %s Full Signature at offset %s !!/n"%(sig_hex[Bingo],sig_name,sig_hex,start))
                    print("/n!! Found %s %s Full Signature at offset %s !!/n"%(sig_hex[Bingo],sig_name,sig_hex,start),file=Logging)
#                    pause=input("BINGO")

                    return 

            start = start + 2
            end = end + 2


Logging = open("Output.log", 'a+')

parser = ArgumentParser()
parser.add_argument("-u","--Url",dest="Source_Sample",help="Url to sample",default=None,metavar="Url")
Args = parser.parse_args()


if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

if Args.Source_Sample is None:
    print("Please provide an url to download sample.\n")
    parser.print_help(sys.stderr)
    sys.exit(1)
else:
     Source_Sample = Args.Source_Sample

##
Origin_Name = "./Sample.origin"
File_Signatures = ["OpenOffice-Header**50 4B 03 04","MsOffice-Header**D0 CF 11 E0 A1 B1 1A E1","MsOffice-SubHeader1**09 08 10 00 00 06 05 00","MsOffice-SubHeader2**FD FF FF FF 10","MsOffice-SubHeader3**FD FF FF FF 1F","MsOffice-SubHeader4**FD FF FF FF 22","MsOffice-SubHeader5**FD FF FF FF 23","MsOffice-SubHeader6**FD FF FF FF 28","MsOffice-SubHeader7**FD FF FF FF 29"]
##

Offset_Similarity = []
Hex_Similarity = []

Origin_Data,Matching_Goal = LoadInput(Origin_Name)
File_Result = DotFilling(Origin_Data)
Similarity()

print("All Done \nNow Proceeding to save it all.\n")
print("All Done \nNow Proceeding to save it all.\n",file=Logging)
SaveOutput("".join(File_Result))
print("\nSee you space cowboy...\n")
print("\nSee you space cowboy...\n",file=Logging)


#Try=0
#Max=13000
#SigSeeker(File_Signatures,Origin_Data)
#while True:
#   if "." not in File_Result:
#         break
#   if Try >= Max:
#       break
#   else:
#       Try = Try +1
#       New_Sample=GetNewSample(Source_Sample).hex()
#       New_Sample2=GetNewSample(Source_Sample).hex()
#       LenCheck(New_Sample,New_Sample2)
#       HexDiff(New_Sample,New_Sample2) 
