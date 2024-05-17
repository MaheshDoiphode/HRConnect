import os
import pandas as pd
import re

root_dir = '.'  # specify your root directory here
emails = []
share_cv_rows = []

# Traverse through all files
for dirpath, dirs, files in os.walk(root_dir):
    for filename in files:
        if filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(dirpath, filename))
            if 'Comment' in df.columns:
                filtered_comments = df[df['Comment'].str.contains("@", na=False)]['Comment'].tolist()
                for comment in filtered_comments:
                    # Extract email addresses using regex
                    matches = re.findall(r'[\w\.-]+@[\w\.-]+', comment)
                    for match in matches:
                        # If email contains '.com' but not ends with '.com', strip it until '.com'
                        if '.com' in match and not match.endswith('.com'):
                            match = match[:match.index('.com')+4]
                        emails.append(match)
                
                # If the comment contains "DM" (ignoring case), store the "Profile link" and "Comment"
                dm_comments = df[df['Comment'].str.contains("DM", na=False, case=False)][['Profile link', 'Comment']].values.tolist()
                share_cv_rows.extend(dm_comments)
                
                # If the comment contains both "Share" and "CV", store the "Profile link" and "Comment"
                share_cv_comments = df[(df['Comment'].str.contains("Share", na=False) & df['Comment'].str.contains("CV", na=False)) & ~df['Comment'].str.contains("DM", na=False, case=False)][['Profile link', 'Comment']].values.tolist()
                share_cv_rows.extend(share_cv_comments)

# Convert lists to DataFrames
emails_df = pd.DataFrame(emails, columns=['Email'])
share_cv_df = pd.DataFrame(share_cv_rows, columns=['Profile link', 'Comment'])

# If CSV files exist, read the existing data, append the new data, and drop duplicates. Otherwise, create new CSV files
if os.path.isfile('emails.csv'):
    existing_emails_df = pd.read_csv('emails.csv')
    combined_emails_df = pd.concat([existing_emails_df, emails_df]).drop_duplicates()
    combined_emails_df.to_csv('emails.csv', index=False)
else:
    emails_df.to_csv('emails.csv', index=False)

if os.path.isfile('share_cv.csv'):
    existing_share_cv_df = pd.read_csv('share_cv.csv')
    combined_share_cv_df = pd.concat([existing_share_cv_df, share_cv_df]).drop_duplicates()
    combined_share_cv_df.to_csv('share_cv.csv', index=False)
else:
    share_cv_df.to_csv('share_cv.csv', index=False)