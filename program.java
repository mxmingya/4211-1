package timeOutExampleJava;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.security.MessageDigest;
import java.util.Random;

/**
 * Created by mingyama on 11/1/16.
 */
public class program {
    public static void main(String[] args) throws IOException {

    }

    private void startServer(String host, Integer port) throws IOException {
        //port = 5001;
        ServerSocket welcomeSock = null;

        try {
            welcomeSock = new ServerSocket(port);
        } catch (Exception e) {
            System.out.println("Error: cannot open socket");
            System.exit(1); // Handle exceptions.
        }

        System.out.println("Server is listening on port 5001...");

        Socket sSock = welcomeSock.accept();
        try{
            BufferedReader inFromClient = new BufferedReader(new InputStreamReader(sSock.getInputStream()));
            PrintWriter sendOut = new PrintWriter(sSock.getOutputStream(), true);

            while(true){
                String data = inFromClient.readLine();


            }

        } catch(Exception e){
            // Do nothing here.
        }

    }

    private void startClient(String host, Integer port, File file ) throws IOException {
        host = "localhost"; // Remote hostname. It can be changed to anything you desire.
        port = 5002; // Port number.
        String sentence; // Store user input.
        String data; // Store the server's feedback.

        Socket cSock = null;
        DataOutputStream sendOutToServer = null;
        BufferedReader readFromServer = null;

        try{
            cSock = new Socket(host, port); // Initialize the socket.
            sendOutToServer = new DataOutputStream(cSock.getOutputStream()); // The output stream to server.
            readFromServer = new BufferedReader(new InputStreamReader(cSock.getInputStream())); // The input stream from server.
        } catch (Exception e) {
            System.out.println("Error: cannot open socket");
            System.exit(1); // Handle exceptions.
        }


		/* Following part is how to handle timeout event. Please pay attention! */

        while(true){
            sendOutToServer.writeBytes("Test" + "\n");
            cSock.setSoTimeout(5000); // Set the time out in milliseconds.
            try{

                data = readFromServer.readLine();
                System.out.println(data);
            } catch (SocketTimeoutException e) {
                System.out.println("Timeout! Retransmitting...");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public String SHA1(String inputText) {
        byte arr[] = null;

        try{
            MessageDigest m = MessageDigest.getInstance("SHA-1");
            m.update(inputText.getBytes("UTF8"));
            arr = m.digest();
        } catch (Exception e){
        }

        StringBuffer sb = new StringBuffer();
        for (int i = 0; i < arr.length; ++i) {
            sb.append(Integer.toHexString((arr[i] & 0xFF) | 0x100).substring(1,3));
        }
        return sb.toString();
    }

    private String Packet(String data, Integer seqNo, Integer isLast) {

        return "";
    }

    private String[] parsePacket(String packet) {
        String[] returnPacket = new String[6];

        return returnPacket;
    }



}
