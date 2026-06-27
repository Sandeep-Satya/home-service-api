import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav style={{
      backgroundColor: '#1a1a2e',
      padding: '1rem 2rem',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <Link to="/" style={{ color: '#e94560', fontSize: '1.5rem', fontWeight: 'bold', textDecoration: 'none' }}>
        🔧 HomeServices
      </Link>
      <div style={{ display: 'flex', gap: '2rem' }}>
        <Link to="/" style={linkStyle}>Home</Link>
        <Link to="/services" style={linkStyle}>Services</Link>
        <Link to="/bookings" style={linkStyle}>My Bookings</Link>
      </div>
    </nav>
  )
}

const linkStyle = {
  color: '#ffffff',
  textDecoration: 'none',
  fontSize: '1rem',
  fontWeight: '500'
}

export default Navbar
