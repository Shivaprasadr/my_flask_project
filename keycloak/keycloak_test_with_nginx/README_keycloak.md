To set up Keycloak in Docker for both user management and as an authentication provider (login page) for your website, you’ll need to configure Keycloak along with a database to store user data and settings. Here’s a step-by-step guide:

### Step 1: Set Up Keycloak with Docker

1. **Create a Docker network** to allow Keycloak and its database to communicate.
   ```bash
   docker network create keycloak-network
   ```

2. **Run a PostgreSQL Database** for Keycloak:
   - You can use PostgreSQL as Keycloak’s database, which is a good choice for performance and compatibility.
   - **Note:** This database should be separate from your application's database for security and scalability.

   ```bash
   docker run -d --name keycloak-db \
       --network keycloak-network \
       -e POSTGRES_DB=keycloak \
       -e POSTGRES_USER=keycloak \
       -e POSTGRES_PASSWORD=password \
       postgres:latest
   ```
docker run -d --name keycloak-db --network keycloak-network -e POSTGRES_DB=keycloak -e POSTGRES_USER=keycloak -e POSTGRES_PASSWORD=password postgres:latest

3. **Run Keycloak** and link it to the PostgreSQL container:
   ```bash
   docker run -d --name keycloak \
       --network keycloak-network \
       -p 8080:8080 \
       -e KEYCLOAK_USER=admin \
       -e KEYCLOAK_PASSWORD=admin \
       -e DB_VENDOR=postgres \
       -e DB_ADDR=keycloak-db \
       -e DB_DATABASE=keycloak \
       -e DB_USER=keycloak \
       -e DB_PASSWORD=password \
       quay.io/keycloak/keycloak:latest start-dev
   ```

4. Once Keycloak is up, you can access it at `http://localhost:8080`. The admin console will be available at `http://localhost:8080/admin`.

### Step 2: Configure Keycloak for User Management and Authentication

1. **Login to Keycloak** (use the admin credentials you specified, `admin/admin` in this example).
2. **Create a Realm**:
   - Go to **Master Realm** > **Add Realm** and name it according to your application (e.g., `myapp`).
3. **Create a Client**:
   - Clients represent applications that will use Keycloak for authentication.
   - Go to **Clients** > **Create** and fill out:
     - **Client ID**: e.g., `myapp-client`
     - **Client Protocol**: `openid-connect`
     - **Root URL**: The base URL of your app (e.g., `http://localhost:3000` if running locally).
   - Save and configure:
     - Enable **Standard Flow** to use Keycloak’s authorization code flow.
     - Optionally, set up Redirect URIs to ensure Keycloak only redirects users to valid app URLs.
4. **Create Roles** (optional):
   - Go to **Roles** and define roles (e.g., `user`, `admin`) if you want role-based access control in your app.
5. **Create Users**:
   - Go to **Users** > **Add User**, then add credentials under **Credentials** and assign roles if needed.

### Step 3: Configure Keycloak Database

The database for Keycloak (in this case, `keycloak-db`) should remain separate from your application’s database to keep the authentication and application data isolated. This separation ensures:

- **Security**: Application data isn’t compromised by user management processes and vice versa.
- **Scalability**: The Keycloak database can be scaled independently of the application database.
- **Maintenance**: Allows individual maintenance and migrations without affecting each other.

### Step 4: Configure Your Application to Use Keycloak for Authentication

In your web application:

1. Use **OpenID Connect (OIDC)** or **OAuth 2.0** libraries to integrate with Keycloak. Popular libraries include:
   - **For Node.js**: `passport-keycloak` or `keycloak-connect`.
   - **For Python**: `python-keycloak` or `flask-keycloak`.

2. Set up the following configurations in your app:
   - **Client ID**: The client ID you created (e.g., `myapp-client`).
   - **Client Secret** (if enabled in Keycloak’s client settings).
   - **Authorization URL**: `http://localhost:8080/realms/myapp/protocol/openid-connect/auth`.
   - **Token URL**: `http://localhost:8080/realms/myapp/protocol/openid-connect/token`.
   - **User Info URL**: `http://localhost:8080/realms/myapp/protocol/openid-connect/userinfo`.

3. **Implement Login/Logout** using Keycloak’s endpoints:
   - Redirect users to the **Authorization URL** for login.
   - Use **Keycloak’s API** to verify tokens and retrieve user information.

### Step 5: Optional Configuration for Persistence and Restart

If you want to make Keycloak data persistent between restarts:

1. Add a **volume** for PostgreSQL in your Docker command:
   ```bash
   docker run -d --name keycloak-db \
       --network keycloak-network \
       -v keycloak-db-data:/var/lib/postgresql/data \
       -e POSTGRES_DB=keycloak \
       -e POSTGRES_USER=keycloak \
       -e POSTGRES_PASSWORD=password \
       postgres:latest
   ```
2. Similarly, consider backing up Keycloak configuration if needed.

### Step 6: Running Keycloak and Database on Start (Optional)

You can use `docker-compose` for ease of startup with both containers:

```yaml
version: "3.8"

services:
  keycloak:
    image: quay.io/keycloak/keycloak:latest
    container_name: keycloak
    command:
      - start-dev
    environment:
      KC_DB: postgres
      KC_DB_URL_HOST: postgres
      KC_DB_URL_PORT: 5432
      KC_DB_URL_DATABASE: keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: change_me
      KC_BOOTSTRAP_ADMIN_USERNAME: admin
      KC_BOOTSTRAP_ADMIN_PASSWORD: admin
    ports:
      - "8080:8080"
    depends_on:
      - postgres
    volumes:
      - ./keycloak_data:/opt/keycloak/data
    networks:
      - keycloak-network

  postgres:
    image: postgres:latest
    container_name: keycloak-postgres
    environment:
      POSTGRES_DB: keycloak
      POSTGRES_USER: keycloak
      POSTGRES_PASSWORD: change_me
    ports:
      - "5432:5432"
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
    networks:
      - keycloak-network
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "keycloak", "-d", "keycloak", "-h", "localhost"]
      interval: 10s
      retries: 5
      start_period: 20s
      timeout: 5s


networks:
  keycloak-network:
    driver: bridge

```

### Summary

- **Database**: Set up PostgreSQL as a separate container for Keycloak; it should be isolated from your application database.
- **Keycloak Setup**: Configure realms, clients, roles, and users as needed.
- **App Integration**: Use OIDC/OAuth 2.0 libraries to integrate Keycloak for authentication.
- **Persistence**: Use volumes to persist Keycloak’s PostgreSQL database.


To configure a domain for your Keycloak instance running in Docker and ensure it is production-ready, follow these steps:

---

### **1. Map Your Domain to Your Laptop**
1. **Port Forwarding** (Router Setup):
   - Forward port `8080` (or any custom port Keycloak uses) on your router to your laptop's internal IP.
   - Test by accessing your laptop's public IP: `http://<public-ip>:8080`.

2. **Set DNS Record**:
   - In InfinityFree's DNS settings, configure an A record for your domain pointing to your public IP.
     - Example: `keycloak.example.com -> <your-public-ip>`

3. **Dynamic IP (Optional)**:
   - If your IP is dynamic, consider using a DDNS service like No-IP or DuckDNS to keep your domain updated.

---

### **2. Configure Keycloak's Hostname**
Keycloak needs to know the domain it is serving. Add the following to the Keycloak service in your `docker-compose.yml`:

```yaml
environment:
  KC_HOSTNAME: keycloak.example.com
  KC_HOSTNAME_STRICT: "true"
  KC_HOSTNAME_STRICT_HTTPS: "false" # Set "true" if you use HTTPS
```

This ensures Keycloak uses `keycloak.example.com` in its URLs and for authentication redirection.

---

### **3. Set Up a Reverse Proxy (Recommended for Production)**

1. **Install a Reverse Proxy**:
   - Use Nginx, Traefik, or Apache to act as a reverse proxy in front of Keycloak.
   - Configure the reverse proxy to handle HTTPS, enforce security headers, and forward traffic to the Keycloak container.

2. **Example Nginx Configuration**:
   ```nginx
   server {
       listen 80;
       server_name keycloak.example.com;

       location / {
           proxy_pass http://localhost:8080;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable HTTPS**:
   - Obtain an SSL certificate from Let's Encrypt using tools like Certbot.
   - Update your reverse proxy to listen on port 443 and serve HTTPS traffic.

---

### **4. Restart Services**
After making these changes:
1. Restart the Docker containers:
   ```bash
   docker-compose down && docker-compose up -d
   ```
2. Restart your reverse proxy service if applicable:
   ```bash
   sudo systemctl restart nginx
   ```

---

### **5. Test Configuration**
- Access Keycloak using your domain: `http://keycloak.example.com`.
- If using HTTPS, ensure `https://keycloak.example.com` is working correctly.

---

Let me know if you need help with any specific configuration!


NOTE:
command to execute the docker compose:
docker-compose down -v
docker-compose up --build -d --force-recreate