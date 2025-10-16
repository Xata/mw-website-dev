Title: Making Zammad Play Nice with Keycloak Groups
Author: Maciej
Date: 2025-10-09 14:00
Category: blog
Tags: zammad, keycloak, oidc, authentication, ruby, sysadmin
Summary: Building automatic role assignment for Zammad using JWT tokens and a cron job

# Making Zammad Play Nice with Keycloak Groups

I recently spent way too much time figuring out how to make Zammad automatically assign roles based on Keycloak groups. Turns out, Zammad's OIDC integration doesn't do this out of the box. Every user who logs in via SS (OIDC) gets stuck with the "Customer" role, regardless of what groups they're in.

## The Problem

Here's the setup: Zammad for ticketing, Keycloak for identity management, OIDC to tie them together. Users can log in just fine, but Zammad has no idea if they're supposed to be an admin, an agent, or just a customer. It just defaults everyone to "Customer".

I needed users in specific Keycloak groups (like `/admins` or `/support/tier2`) to automatically get the right Zammad roles. No manual clicking around in the admin panel after every new user signs in. I really didn't want to be the one doing that. I needed automation.

## Why This Matters

If you're running a helpdesk or support system with tiered access (tier 1 support, tier 2, admins, etc.), you don't want to manually assign Zammad roles every time someone new logs in. You want it to just work based on your existing identity provider. So you can go do other things with your life.

Keycloak already knows who's who. Zammad really really should too.

## The Solution

Since Zammad doesn't natively support this, I wrote a Ruby script that:

1. Decodes the JWT token from OIDC authentication
2. Extracts the `groups` claim from Keycloak
3. Maps those groups to Zammad roles
4. Runs automatically via cron every 5 minutes

The script lives on the Zammad server and syncs roles in the background. Works great.

## How It Works

### Step 1: Configure Keycloak

First, make sure your Keycloak client is sending group information in the token. You need a **Groups Mapper**:

- Mapper Type: `Group Membership`
- Token Claim Name: `groups`
- Add to ID token: ✓
- Add to access token: ✓
- Add to userinfo: ✓

This tells Keycloak to include group memberships in the JWT token when users authenticate.

### Step 2: Enable OIDC in Zammad

SSH into your Zammad server and open the Rails console:

```bash
sudo zammad run rails c
```

Configure OIDC:

```ruby
# Enable OIDC
Setting.set('auth_openid_connect', true)

# Configure credentials
config = Setting.get('auth_openid_connect_credentials')
config[:display_name] = 'SSO Login'
config[:identifier] = 'zammad-client'
config[:issuer] = 'https://your-keycloak-server/realms/your-realm'
config[:uid_field] = 'preferred_username'
config[:scope] = 'openid email profile'

Setting.set('auth_openid_connect_credentials', config)
```

Replace `your-keycloak-server` and `your-realm` with your actual Keycloak URL and realm name.

### Step 3: Decode the JWT to See What You're Working With

Before writing the sync script, you need to see what Keycloak is actually sending. In the Rails console:

```ruby
# Find a user who logged in via OIDC
user = User.find_by(login: 'someone@example.com')
auth = user.authorizations.where(provider: 'openid_connect').first

# Decode the JWT token
require 'json'
require 'base64'

parts = auth.token.split('.')
payload = parts[1]
payload += '=' * (4 - payload.length % 4) if payload.length % 4 != 0

decoded = JSON.parse(Base64.urlsafe_decode64(payload))
decoded['groups']
```

This will show you the exact format of the groups. Something like:

```ruby
["/admins", "/support/tier1", "/support/tier2"]
```

### Step 4: Create Zammad Roles

Make sure you have the roles you need in Zammad. Go to **Admin → Manage → Roles** and create:

- `Admin` (should already exist)
- `Agent` (should already exist)
- `Customer` (default)
- Any custom roles (like `tier1`, `tier2`, etc.)

### Step 5: Write the Sync Script

Create the script on your Zammad server:

```bash
sudo nano /opt/zammad/script/sync_oidc_roles.rb
```

Here's the script (adjust the group-to-role mapping for your setup):

```ruby
#!/usr/bin/env ruby
# Sync OIDC user roles based on Keycloak groups

require '/opt/zammad/config/environment'

User.where(source: 'openid_connect').find_each do |user|
  auth = user.authorizations.where(provider: 'openid_connect').first
  next unless auth&.token

  require 'json'
  require 'base64'

  parts = auth.token.split('.')
  payload = parts[1]
  payload += '=' * (4 - payload.length % 4) if payload.length % 4 != 0

  begin
    decoded = JSON.parse(Base64.urlsafe_decode64(payload))
    groups = decoded['groups'] || []

    roles_to_assign = []

    # Map Keycloak groups to Zammad roles
    if groups.include?('/admins')
      roles_to_assign += ['Admin', 'Agent']
    elsif groups.include?('/support/tier3')
      roles_to_assign += ['Agent', 'tier3']
    elsif groups.include?('/support/tier2')
      roles_to_assign += ['Agent', 'tier2']
    elsif groups.include?('/support/tier1')
      roles_to_assign += ['Agent', 'tier1']
    else
      roles_to_assign = ['Customer']
    end

    if roles_to_assign.any?
      role_objects = Role.where(name: roles_to_assign.uniq)
      current_roles = user.roles.pluck(:name)

      unless (current_roles.sort == roles_to_assign.sort)
        user.role_ids = role_objects.pluck(:id)
        user.save!
        puts "Updated #{user.login}: #{roles_to_assign.join(', ')}"
      end
    end
  rescue => e
    puts "Error for #{user.login}: #{e.message}"
  end
end
```

Make it executable:

```bash
sudo chmod +x /opt/zammad/script/sync_oidc_roles.rb
sudo chown zammad:zammad /opt/zammad/script/sync_oidc_roles.rb
```

### Step 6: Test It

Run the script manually:

```bash
sudo zammad run ruby /opt/zammad/script/sync_oidc_roles.rb
```

You should see output like:

```
Updated user@example.com: Agent, tier2
Updated admin@example.com: Admin, Agent
```

### Step 7: Automate with Cron

Edit root's crontab:

```bash
sudo crontab -e
```

Add this line to run the script every 5 minutes:

```
*/5 * * * * /usr/bin/zammad run ruby /opt/zammad/script/sync_oidc_roles.rb >> /var/log/zammad/sync_roles.log 2>&1
```

Save and exit. Now the script runs automatically.

## Things to Know

**JWT tokens expire:** The script reads the stored token, which eventually expires. Users need to log out and back in periodically to refresh their token (and by extension, their groups). The cron job picks up changes within 5 minutes after a fresh login.

**Group changes require re-login:** If you change someone's groups in Keycloak, they won't see the change in Zammad until they log out and back in (so the token refreshes).

**Customizing the mapping:** Just edit the `if`/`elsif` logic in the script. Match it to your Keycloak group structure and Zammad role names.

**Performance:** The script loops through all OIDC users. If you have thousands of users, you might want to optimize it or run it less frequently.

## Conclusion

This was one of those problems where the official integration gets you 80% of the way there, but the last 20% requires some DIY work. Once it's set up though, it works great. Users log in via SSO and automatically get the right permissions based on their groups.

If you're running Zammad with Keycloak (or any OIDC provider that sends group claims), this approach should work for you. Just adjust the group names and role mappings to fit your setup.

Thanks for reading!
