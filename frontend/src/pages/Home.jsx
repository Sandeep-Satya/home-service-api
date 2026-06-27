import { useNavigate } from 'react-router-dom'

function Home() {
  const navigate = useNavigate()

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#0f0f1a',
      color: '#ffffff',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      textAlign: 'center',
      padding: '2rem'
    }}>
      <h1 style={{ fontSize: '3rem', color: '#e94560', marginBottom: '1rem' }}>
        🔧 Home Services
      </h1>
      <p style={{ fontSize: '1.2rem', color: '#aaaaaa', maxWidth: '600px', marginBottom: '2rem' }}>
        Find trusted local professionals for all your home needs —
        plumbers, electricians, painters, AC technicians and more.
        Book an appointment in seconds.
      </p>
      <button
        onClick={() => navigate('/services')}
        style={{
          backgroundColor: '#e94560',
          color: '#ffffff',
          border: 'none',
          padding: '1rem 2.5rem',
          fontSize: '1.1rem',
          borderRadius: '8px',
          cursor: 'pointer',
          fontWeight: 'bold'
        }}
      >
        Book a Service
      </button>
    </div>
  )
}

export default Home
