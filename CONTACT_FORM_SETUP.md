# Contact Form Setup Instructions

The contact form on the LoRaLeaf website is configured to send emails to **info@loraleaf.com** using Formspree.

## One-Time Setup Required

**Important:** The first time someone submits the contact form, Formspree will send a **confirmation email to info@loraleaf.com**. You MUST click the confirmation link in that email to activate the form.

### Steps:

1. **Wait for a form submission** (or submit a test yourself from the website)
2. **Check info@loraleaf.com inbox** for an email from Formspree
3. **Click the confirmation link** in the email
4. Done! All future submissions will be sent directly to info@loraleaf.com

### What Happens After Activation:

- Form submissions automatically emailed to info@loraleaf.com
- You'll receive sender's name, email, organization, and message
- The sender's email will be in the "Reply-To" field for easy responses
- Free tier allows 50 submissions/month (more than enough to start)

### Alternative: Create a Free Formspree Account

If you want more control (spam filtering, file uploads, etc.):

1. Go to https://formspree.io
2. Sign up with info@loraleaf.com
3. Create a new form
4. Copy the form ID (looks like `xannpazp`)
5. Update `index.html` line 351:
   ```html
   <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
   ```
   Replace `info@loraleaf.com` with your actual form ID

## Testing

To test the form:
1. Visit https://blue-glacier-0ff05ed03.3.azurestaticapps.net
2. Scroll to "Contact" section
3. Fill out the form and submit
4. Check info@loraleaf.com for the confirmation email (first time only)
5. Click the confirmation link
6. Test again - you should receive the message directly

## Troubleshooting

- **Not receiving emails?** Check spam folder in info@loraleaf.com
- **Form not working?** Ensure you clicked the confirmation link
- **Want to change email?** Update line 351 in index.html with new email address

## Support

Formspree documentation: https://help.formspree.io/
