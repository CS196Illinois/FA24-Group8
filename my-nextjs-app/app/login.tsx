import React from 'react';
import Head from 'next/head';
import Link from 'next/link';

const Login: React.FC = () => {
  return (
    <>
      <Head>
        <title>Login | Nexus Scholar</title>
      </Head>
      <div className="login-container">
        <div className="logo">
          {/* Assuming you have a logo as an image or component */}
          <h1>Nexus Scholar</h1>
        </div>
        <h2>Log in to Nexus Scholar</h2>
        <form className="login-form">
          <label htmlFor="email">Email</label>
          <input type="email" id="email" placeholder="name@example.com" required />
          
          <label htmlFor="password">Password</label>
          <input type="password" id="password" placeholder="Enter your password" required />
          
          <button type="submit" className="login-button">Log In</button>
        </form>
        <div className="links">
          <Link href="/forgot-password">
            <a className="forgot-password">Forgot password?</a>
          </Link>
          <p>
            Don’t have an account?{' '}
            <Link href="/signup">
              <a className="signup-link">Sign up</a>
            </Link>
          </p>
        </div>
      </div>
      <style jsx>{`
        /* Page Styling */
        body {
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          background-color: #121212;
          color: #fff;
          font-family: Arial, sans-serif;
        }

        .login-container {
          max-width: 400px;
          width: 100%;
          padding: 40px;
          background-color: #181818;
          border-radius: 8px;
          text-align: center;
          box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
        }

        .logo h1 {
          font-size: 24px;
          margin-bottom: 16px;
          color: #fff;
        }

        h2 {
          font-size: 20px;
          margin-bottom: 24px;
        }

        .login-form {
          display: flex;
          flex-direction: column;
          align-items: stretch;
        }

        label {
          text-align: left;
          font-size: 14px;
          margin-bottom: 6px;
          color: #cccccc;
        }

        input {
          padding: 10px;
          margin-bottom: 20px;
          border-radius: 4px;
          border: none;
          background-color: #282828;
          color: #fff;
          font-size: 16px;
        }

        input::placeholder {
          color: #7a7a7a;
        }

        .login-button {
          padding: 12px;
          background-color: #ffffff;
          color: #121212;
          border: none;
          border-radius: 4px;
          font-size: 16px;
          cursor: pointer;
          transition: background 0.3s;
        }

        .login-button:hover {
          background-color: #cccccc;
        }

        .links {
          margin-top: 20px;
          font-size: 14px;
        }

        .forgot-password, .signup-link {
          color: #a0a0a0;
          text-decoration: none;
          transition: color 0.3s;
        }

        .forgot-password:hover, .signup-link:hover {
          color: #ffffff;
        }
      `}</style>
    </>
  );
};

export default Login;
