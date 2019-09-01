import java.awt.*;
import java.awt.event.*;
import java.net.*;

import javax.swing.*;
import javax.swing.event.*;
class ticTacClient{

    static Socket sock;
    static int port;

    public static void main(String args[]){
       JFrame frame = new JFrame("tic-tac");
       frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
       frame.setSize(600, 595);
       
       //North area, where the user will connect
       JPanel northPanel = new JPanel();       
       JTextField addressField = new JTextField(33);
       JTextField portField = new JTextField(5);
       JButton connectButton = new JButton("Connect");
       addressField.setText("127.0.0.1");
       portField.setText("6969");
       northPanel.add(addressField);
       northPanel.add(portField);
       northPanel.add(connectButton);

       //The main area of text
       JPanel centerPanel = new JPanel();  
       JTextArea textBox = new JTextArea(30, 47);
       JScrollPane scrollPane = new JScrollPane(textBox);
       scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
       textBox.setEditable(false);
       centerPanel.add(scrollPane);

       //South area, with the message field and send button
       JPanel southPanel = new JPanel();
       JTextField messageField = new JTextField(42);
       JButton sendButton = new JButton("Enter");
       messageField.setEnabled(false);
       sendButton.setEnabled(false);
       southPanel.add(messageField);
       southPanel.add(sendButton);

       frame.getContentPane().add(BorderLayout.NORTH, northPanel);
       //frame.getContentPane().add(BorderLayout.CENTER, textBox);
       frame.getContentPane().add(BorderLayout.CENTER, centerPanel);
       frame.getContentPane().add(BorderLayout.SOUTH, southPanel);
       frame.setVisible(true);

       connectButton.setMnemonic(KeyEvent.VK_ENTER);
       connectButton.addActionListener(connect());
       
    }

    public static ActionListener connect(){
        return new ActionListener(){
            public void actionPerformed(ActionEvent e) {
                try { port = Integer.parseInt(portField.getText()); }
                catch(Exception ex) { textBox.append("Invalid Port\n"); return; }
                try { sock = new Socket(addressField.getText(), port); }
                catch(Exception ex) { textBox.append("Couldn't connect\n"); return; }
                portField.setEnabled(false);
                addressField.setEnabled(false);
                connectButton.setText("Leave");
                connectButton.removeActionListener(this);
                connectButton.addActionListener(new ActionListener());
            }
        };
    }
}