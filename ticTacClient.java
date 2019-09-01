import java.awt.*;
import java.awt.event.*;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;
import java.util.Arrays;
import java.util.Scanner;

import javax.swing.*;
import javax.swing.event.*;
class ticTacClient{

    static Socket sock;
    static int port;
    static Thread thread;
    static ActionEventListener connector = connect();
    static ActionEventListener leaver = leave();
    static ActionEventListener sender = send();

    static JButton connectButton;
    static JTextField addressField;
    static JTextField portField;

    static JTextArea textBox;

    static JTextField messageField;
    static JButton sendButton;

    public static void main(String args[]){
       JFrame frame = new JFrame("tic-tac");
       frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
       frame.setSize(600, 595);
       
       //North area, where the user will connect
       JPanel northPanel = new JPanel();       
       addressField = new JTextField(34);
       portField = new JTextField(5);
       connectButton = new JButton("Connect");
       addressField.setText("127.0.0.1");
       portField.setText("6969");
       northPanel.add(addressField);
       northPanel.add(portField);
       northPanel.add(connectButton);

       //The main area of text
       JPanel centerPanel = new JPanel();  
       textBox = new JTextArea(30, 47);
       JScrollPane scrollPane = new JScrollPane(textBox);
       scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
       textBox.setEditable(false);
       centerPanel.add(scrollPane);

       //South area, with the message field and send button
       JPanel southPanel = new JPanel();
       messageField = new JTextField(40);
       sendButton = new JButton("Enter");
       messageField.setEnabled(false);
       sendButton.setEnabled(false);
       southPanel.add(messageField);
       southPanel.add(sendButton);

       frame.getContentPane().add(BorderLayout.NORTH, northPanel);
       //frame.getContentPane().add(BorderLayout.CENTER, textBox);
       frame.getContentPane().add(BorderLayout.CENTER, centerPanel);
       frame.getContentPane().add(BorderLayout.SOUTH, southPanel);
       frame.setVisible(true);

       connectButton.addActionListener(connector);
       sendButton.addActionListener(send());
    }

    public static ActionListener connect(){
        return new ActionListener(){

            @Override
            public void actionPerformed(ActionEvent e) {
                try { port = Integer.parseInt(portField.getText()); }
                catch(Exception ex) { textBox.append("Invalid Port\n"); return; }
                try { sock = new Socket(addressField.getText(), port); }
                catch(Exception ex) { textBox.append("Couldn't connect\n"); return; }
                portField.setEnabled(false);
                addressField.setEnabled(false);
                messageField.setEnabled(true);
                sendButton.setEnabled(true);
                connectButton.setText("Leave");
                connectButton.removeActionListener(connector);
                connectButton.addActionListener(leaver);
                thread = new Thread(new Receiver());
                thread.start();
            }
        };
    }

    public static void resetUI(){
        portField.setEnabled(true);
        addressField.setEnabled(true);
        messageField.setEnabled(false);
        sendButton.setEnabled(false);
        connectButton.setText("Connect");
        connectButton.removeActionListener(leaver);
        connectButton.addActionListener(connector);
        thread.stop();
    }

    public static ActionListener leave(){
        return new ActionListener(){
        
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    sock.getOutputStream().write("!leave".getBytes());
                    sock.getOutputStream().flush();
                    wait(50);
                    sock.getOutputStream().write("!quit".getBytes());
                    sock.getOutputStream().flush();
                    wait(50);
                    sock.close();
                    sock = null;
                } catch(Exception ex) {
                    textBox.append(ex.getMessage());
                }
                resetUI();
            }
        };
    }

    public static ActionListener send(){
        return new ActionListener(){
        
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    sock.getOutputStream().write(messageField.getText().getBytes());
                    sock.getOutputStream().flush();
                } catch(Exception ex) {
                    textBox.append(ex.getMessage());
                    resetUI();
                }
                messageField.setText("");
            }
        };
    }

    public static class Receiver implements Runnable {
        public void run() {
            try {
                Scanner in = new Scanner(sock.getInputStream());
                try {
                    while(in.hasNextLine()){
                        textBox.append(in.nextLine() + "\n");
                    }
                } catch(Exception ex) {
                    textBox.append(ex.getMessage());
                } finally {
                    in.close();
                }
            } catch(Exception ex) {
                textBox.append(ex.getMessage());
            }
        }
    }
}