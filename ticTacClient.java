import java.awt.*;
import java.awt.event.*;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;
import java.util.Arrays;
import java.util.Scanner;
import javax.swing.*;
import javax.swing.AbstractAction;
import javax.swing.KeyStroke;
import javax.swing.event.*;
import javax.swing.text.DefaultCaret;

class ticTacClient{

    static Socket sock;
    static int port;
    static Thread thread;
    static ActionListener connector = connect();
    static ActionListener sender = send();
    static KeyListener enterer = enter();

    static JButton connectButton;
    static JTextField addressField;
    static JTextField portField;

    static JTextArea textBox;

    static JTextField messageField;
    static JButton sendButton;

    public static void main(String args[]){
       JFrame frame = new JFrame("tic-tac");
       frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
       frame.setSize(605, 588);
       
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
       DefaultCaret caret = (DefaultCaret)textBox.getCaret();
       caret.setUpdatePolicy(DefaultCaret.ALWAYS_UPDATE);
       textBox.setEditable(false);
       centerPanel.add(scrollPane);

       //South area, with the message field and send button
       JPanel southPanel = new JPanel();
       messageField = new JTextField(42);
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
       sendButton.addActionListener(sender);
       messageField.addKeyListener(enterer);
    }

    public static KeyListener enter() {
        return new KeyListener(){

            public void keyTyped(KeyEvent e) {
                //nothing
            }

            @Override
            public void keyPressed(KeyEvent e) {
                if(e.getKeyCode() == KeyEvent.VK_ENTER){
                    sendButton.doClick();
                }
            }

            public void keyReleased(KeyEvent e) {
                //nothing
            }
        };
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
                connectButton.setEnabled(false);
                messageField.requestFocus();
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
        connectButton.setEnabled(true);
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
                    resetUI();
                    textBox.append("Exited\n");
                }
            } catch(Exception ex) {
                textBox.append(ex.getMessage());
            }
        }
    }
}