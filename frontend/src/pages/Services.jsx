import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

function Services() {
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetch('http://34.234.44.64/services')
      .then(res => res.json())
      .then(data => {
        setServices(data)
        setLoading(false)
      })
  }, [])

  if (loading) return <p style={{ color: '#fff', textAlign: 'center', marginTop: '2rem' }}>Loading services...</p>

  return (
    <div style={{ backgroundColor: '#0f0f1a', minHeight: '100vh', padding: '2rem' }}>
      <h2 style={{ color: '#e94560', textAlign: 'center', marginBottom: '2rem' }}>Available Services</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', maxWidth: '900px', margin: '0 auto' }}>
        {services.map(service => (
          <div
            key={service.id}
            onClick={() => navigate(`/book/${service.id}`, { state: { serviceName: service.name } })}
            style={{
              backgroundColor: '#1a1a2e',
              border: '1px solid #e94560',
              borderRadius: '12px',
              padding: '2rem',
              textAlign: 'center',
              cursor: 'pointer',
              color: '#ffffff',
              fontSize: '1.1rem',
              fontWeight: 'bold',
              transition: 'transform 0.2s'
            }}
            onMouseOver={e => e.currentTarget.style.transform = 'scale(1.05)'}
            onMouseOut={e => e.currentTarget.style.transform = 'scale(1)'}
          >
            🔧 {service.name}
          </div>
        ))}
      </div>
    </div>
  )
}

export default Services
