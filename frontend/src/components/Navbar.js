import { Link } from "react-router-dom";
import logo from "../streak.jpeg";
export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-logo">
          <img src={logo} alt="StreakForge Logo" classname="logo-img"/>
      </div>
      
      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/support">Support</Link>
        <Link to="/login">Login</Link>
        <Link to="/signup">Signup</Link>
      </div>
    </nav>
  );
}
