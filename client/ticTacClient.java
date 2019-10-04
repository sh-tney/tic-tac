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

/**
 * A simple client application to host a TCP text connection, connecting to the
 * specified address and port, closing the connection on closing the app. If
 * the connection closes from the server side, the client will become inactive
 * until the user connects to a host again. Once connected, the client acts
 * as a simple text relayer, sending text when the user presses enter or the
 * send button, and constantly streaming incoming messages from another thread.
 */
class ticTacClient{

    //Some global variables, mostly for housing 
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
       addressField = new JTextField(60);
       portField = new JTextField(6);
       connectButton = new JButton("Connect");
       addressField.setText("ec2-3-94-209-229.compute-1.amazonaws.com");
       addressField.setFont(new Font("monospaced", Font.PLAIN, 12));
       portField.setFont(new Font("monospaced", Font.PLAIN, 12));
       portField.setText("6969");
       northPanel.add(addressField);
       northPanel.add(portField);
       northPanel.add(connectButton);

       //The main area of text
       JPanel centerPanel = new JPanel();  
       textBox = new JTextArea(32, 80);
       JScrollPane scrollPane = new JScrollPane(textBox);
       scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
       textBox.setFont(new Font("monospaced", Font.PLAIN, 12));
       //DefaultCaret caret = (DefaultCaret)textBox.getCaret();
       //caret.setUpdatePolicy(DefaultCaret.ALWAYS_UPDATE);
       textBox.setEditable(false);
       centerPanel.add(scrollPane);

       //South area, with the message field and send button
       JPanel southPanel = new JPanel();
       messageField = new JTextField(71);
       messageField.setFont(new Font("monospaced", Font.PLAIN, 12));
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

    /**
     * Returns a new KeyListener event, listening for the enter key press
     * and then executing a "click" on the send button.
     */
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

    /**
     * This creates the action listener to handle the connect button's function
     * Attempting to connect to the host, and simply notifying the user if the 
     * host or port is invalid, or unreachable.
     */
    public static ActionListener connect(){
        return new ActionListener(){

            @Override
            public void actionPerformed(ActionEvent e) {
                try { 
                    port = Integer.parseInt(portField.getText()); 
                }
                catch(Exception ex) { 
                    textBox.append("Invalid Port\n"); return; 
                }

                try { 
                    sock = new Socket(addressField.getText(), port); 
                }
                catch(Exception ex) { 
                    textBox.append("Couldn't connect\n"); return; 
                }
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

    /**
     * Consolidation of the various UI feature changes needed when a connection
     * is either closed or lost.
     */
    public static void resetUI(){
        portField.setEnabled(true);
        addressField.setEnabled(true);
        messageField.setEnabled(false);
        sendButton.setEnabled(false);
        connectButton.setEnabled(true);
    }

    /**
     * The listener for the send button, executing the sending of whatever is 
     * currently in the text box
     */
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

    /**
     * A runnable class to be used in a seperate thread, to be constantly
     * listening and recieving for new messages from the active host. When the
     * connection closes, and therefore the InputStream reaches end of file, 
     * socket is closed, and the UI is reset, and then the thread ends.
     */
    public static class Receiver implements Runnable {
        public void run() {
            try {
                Scanner in = new Scanner(sock.getInputStream());
                try {
                    while(in.hasNextLine()){
                        textBox.append(in.nextLine() + "\n");
                        textBox.setCaretPosition(textBox.getDocument().getLength());
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