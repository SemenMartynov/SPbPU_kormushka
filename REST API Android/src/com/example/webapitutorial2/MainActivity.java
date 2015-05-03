package com.example.webapitutorial2;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;
import org.xmlpull.v1.XmlPullParserFactory;

import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.view.Menu;
import android.view.View;
import android.widget.EditText;

public class MainActivity extends Activity {

	public final static String strikeIronUserName = "username@yourdomain.com";
	public final static String strikeIronPassword = "password";
	public final static String apiURL = "http://ws.strikeiron.com/StrikeIron/EMV6Hygiene/VerifyEmail?";
	public final static String EXTRA_MESSAGE = "com.example.webapitutorial.MESSAGE";
	
	private class emailVerificationResult {
		public String statusNbr;
		public String hygieneResult;	
	}
	
	private class CallAPI extends AsyncTask<String, String, String> {
    	
		
	    @Override
	    protected String doInBackground(String... params) {
	      String urlString=params[0]; // URL to call
	      String resultToDisplay = "";
	      InputStream in = null;
	      emailVerificationResult result = null;
	        
	      // HTTP Get
	      try {
	        URL url = new URL(urlString);
	    	HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
	    	in = new BufferedInputStream(urlConnection.getInputStream());
	      } catch (Exception e ) {
	        System.out.println(e.getMessage());
	    	return e.getMessage();
	      }
	    	   
	       // Parse XML
	       XmlPullParserFactory pullParserFactory;
	       try {
	    	    pullParserFactory = XmlPullParserFactory.newInstance();
	    	    XmlPullParser parser = pullParserFactory.newPullParser();
	    	    parser.setFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES, false); 
	    	    parser.setInput(in, null);
	    	    result = parseXML(parser);
	       } catch (XmlPullParserException e) {
	    	   e.printStackTrace();
	       } catch (IOException e) {
	    	   e.printStackTrace();
	       }

	       // Simple logic to determine if the email is dangerous, invalid, or valid
	       if (result != null ) {
	         if( result.hygieneResult.equals("Spam Trap")) {
	    	   resultToDisplay = "Dangerous email, please correct";
	    	 }
	    	 else if( Integer.parseInt(result.statusNbr) >= 300) {
	    	   resultToDisplay = "Invalid email, please re-enter";
	    	 }
	    	 else {
	    	   resultToDisplay = "Thank you for your submission";
	    	 }
	    		
	       }
	       else {
	         resultToDisplay = "Exception Occured";
	       }
	     
	       return resultToDisplay;
   
	    }

	    protected void onPostExecute(String result) {
	        Intent intent = new Intent(getApplicationContext(), ResultActivity.class); 
	   		intent.putExtra(EXTRA_MESSAGE, result);
	    	startActivity(intent);
	    }
	    
	    private emailVerificationResult parseXML( XmlPullParser parser ) throws XmlPullParserException, IOException {
	      int eventType = parser.getEventType();
	      emailVerificationResult result = new emailVerificationResult(); 
	        
	      while( eventType!= XmlPullParser.END_DOCUMENT) {
	      String name = null;
	      switch(eventType)
	      {
	        case XmlPullParser.START_TAG:
	      	  name = parser.getName();
	      	  if( name.equals("Error")) {
	      	    System.out.println("Web API Error!");
	      	  }
	      	  else if ( name.equals("StatusNbr")) {
	      	    result.statusNbr = parser.nextText();
	      	  }
	      	  else if (name.equals("HygieneResult")) {
	      	    result.hygieneResult = parser.nextText();
	      	  }
	      	  break;
	      	case XmlPullParser.END_TAG:
	      	  break;
	      	} // end switch
	      	
	      	eventType = parser.next();	
	      } // end while
	        return result;		
	     }


	} // end CallAPI

	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	// This is the method that is called when the submit button is clicked
    public void verifyEmail(View view) {
    	EditText emailEditText = (EditText) findViewById(R.id.email_address);
    	String email = emailEditText.getText().toString();

        if( email != null && !email.isEmpty()) {
 	      String urlString = apiURL + "LicenseInfo.RegisteredUser.UserID=" + strikeIronUserName + "&LicenseInfo.RegisteredUser.Password=" + strikeIronPassword + "&VerifyEmail.Email=" + email + "&VerifyEmail.Timeout=30";
 	      new CallAPI().execute(urlString);	
        }	
 

  
    }

	
}
