import ReedSolomon.ReedSolomon;
import utils.IOUtilities;

import java.io.File;

import javax.sound.sampled.SourceDataLine;

public class Main {
    public static void main(String[] args) {

        //get argument that has been passed from python
        String arg = args[0];

        //tokenize the arguments
        String[] tokens = arg.split(" ");

        String command = tokens[0];
        int N;
        int K;
        if(command.equals("encode")){ //encode filename N K
            String filename = tokens[1];
            N = Integer.parseInt(tokens[2]);
            K = Integer.parseInt(tokens[3]);

            //check if the file exists
            File f = new File(filename);
            if(!f.isFile() || !f.exists()){
                System.out.println("FILE_DOES_NOT_EXIST");
            }else{
                try {
                    //load the file in bytes
                    byte[] allData = new byte[(int) f.length()];
                    IOUtilities.fileToByte(f, 0, (int) f.length(), allData, 0);

                    //perform RS encode
                    byte[][] fragments = erasureCodingEncode(allData, allData.length, K, N);

                    //create /fragmentsDir directory
                    File fragmentsDir = new File("fragments/");
                    if(fragmentsDir.exists()){
                        //list and delete all files in fragments/ directory
                        File[] frags = fragmentsDir.listFiles();
                        for(File fr: frags){                                            
                            fr.delete();
                        } 
                    }else{
                        fragmentsDir.mkdir();
                    }
                    
                    //store the fragments in the /fragmentsDir directory
                    for (int i = 0; i < fragments.length; i++) {
                        IOUtilities.byteToFile_FOS_write(fragments[i], fragmentsDir, Integer.toString(i));
                    }
   
                    System.out.println("SUCCESS");
                }catch(Exception e){
                    System.out.println("EC_FAILURE_EXCEPTION");
                    //e.printStackTrace();
                }
            }
        }else if(command.equals("decode")){  //decode filename N K
            String filename = tokens[1];
            N = Integer.parseInt(tokens[2]);
            K = Integer.parseInt(tokens[3]);

            //check if the fragments directory exists
            File fragmentsDir = new File("fragments/");
            if (!fragmentsDir.exists()) {
                System.out.println("FRAGMENTS_DIR_DOES_NOT_EXIST");
            }else{
                //check if at least K number of fragments are available
                File[] fragments = fragmentsDir.listFiles();
                if(fragments.length<K){
                    System.out.println("NOT_ENOUGH_FRAGMENTS_AVAILABLE");
                }else{
                    byte[] fileBytes = erasureCodingDecode(fragments, N, K);

                    //write the bytes in file
                    File outputPath = new File("actualFile/");
                    if(outputPath.exists()){
                        outputPath.delete();
                        outputPath.mkdir();
                    }
                    File outputFile = IOUtilities.createNewFile("actualFile" + File.separator + filename);
                    IOUtilities.byteToFile_RAF_append(fileBytes, 0, fileBytes.length, outputFile, 0);
                    System.out.println("SUCCESS");
                }
            }
        }
    }


    //takes a bytearray, length of data to be encoded from offset 0, (K,N) values, and returns fragments after performing RS erasure encoding
    public static byte[][] erasureCodingEncode(byte[] allData, int dataLength, int K2, int N2){

        byte[] allBytes = new byte[dataLength ]; //+1
        System.arraycopy(allData, 0, allBytes, 0, dataLength);

        // Figure out how big each shard will be.
        int shardSize = (dataLength + K2 - 1) / K2;

        // Make the buffers to hold the shards.
        byte [] [] shards = new byte [N2] [shardSize];

        // Fill in the data shards
        for (int i = 0; i < K2; i++) {
            System.arraycopy(allBytes, i * shardSize, shards[i], 0, shardSize);
        }

        // Use Reed-Solomon to calculate the parity.
        ReedSolomon reedSolomon = ReedSolomon.create(K2, N2-K2);
        reedSolomon.encodeParity(shards, 0, shardSize);

        //return
        return shards;
    }


    //takes a list of shards as bytearrays, uses erasure coding and
    // returns the decoded bytearray.
    private static byte[] erasureCodingDecode(File[] Fragments, int N2, int K2){

        //create space for file fragments
        byte[][] shards = new byte[N2][];
        boolean[] shardPresent = new boolean[N2];
        int shardCount = 0;
        int shardSize = 0;

        for(File f: Fragments){

            //get bytes from fragments
            byte[] fragBytes = IOUtilities.fileToByte(f);

            //check if the fragment name is numeric, if not, disregard this file
            try {
                double d = Double.parseDouble(f.getName());
            } catch (NumberFormatException nfe) {
                continue;
            }
            
            //get fragment number
            int fragmentIdx = Integer.parseInt(f.getName());

            //populate existing shard indexes with data
            shardSize = fragBytes.length;
            shards[fragmentIdx] = fragBytes;
            shardPresent[fragmentIdx] = true;
            shardCount++;
        }

        //populate other index of shard arrays by 0s
        for (int i = 0; i < N2; i++) {
            if (!shardPresent[i]) {
                shards[i] = new byte[shardSize];
            }
        }

        // Use Reed-Solomon to fill in the missing shards
        ReedSolomon reedSolomon = ReedSolomon.create(K2, N2-K2);
        reedSolomon.decodeMissing(shards, shardPresent, 0, shardSize);

        // Combine the data shards into one buffer for convenience
        byte[] allBytes = new byte[shardSize * K2];
        for (int i = 0; i < K2; i++) {
            System.arraycopy(shards[i], 0, allBytes, shardSize * i, shardSize);
        }

        return allBytes;
    }

}

