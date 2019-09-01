import java.awt.*;
import javax.swing.*;
class ticTacClient{
    public static void main(String args[]){
       JFrame frame = new JFrame("tic-tac");
       frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
       frame.setSize(600,600);
       
       //North area, where the user will connect
       JPanel northPanel = new JPanel();       
       JTextField addressField = new JTextField(33);
       JTextField portField = new JTextField(5);
       JButton connectButton = new JButton("Connect");
       northPanel.add(addressField);
       northPanel.add(portField);
       northPanel.add(connectButton);

       //The main area of text
       JPanel centerPanel = new JPanel();  
       JTextArea textBox = new JTextArea(31, 48);
       centerPanel.add(textBox);

       //South area, with the message field and send button
       JPanel southPanel = new JPanel();
       JTextField messageField = new JTextField(42);
       JButton sendButton = new JButton("Enter");
       southPanel.add(messageField);
       southPanel.add(sendButton);

       frame.getContentPane().add(BorderLayout.NORTH, northPanel);
       //frame.getContentPane().add(BorderLayout.CENTER, textBox);
       frame.getContentPane().add(BorderLayout.CENTER, centerPanel);
       frame.getContentPane().add(BorderLayout.SOUTH, southPanel);
       frame.setVisible(true);
    }
}