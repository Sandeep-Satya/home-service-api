import { useEffect, useState } from 'react'

function Bookings() {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('http://34.234.44.64/bookings')
      .then(res => res.json())
      .then(data => {
        setBookings(data)
        setLoading(false)
      })
  }, [])

  if (loading) return <p style={{ color: '#fff', textAlign: 'center', marginTop: '2rem' }}>Loading...</p>

  if (bookings.length === 0) return (
    <div style={{ backgroundColor: '#0f0f1a', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <p style={{ color: '#aaaaaa', fontSize: '1.2rem' }}>No bookings yet.</p>
    </div>
  )

  return (
    <div style={{ backgroundColor: '#0f0f1a', minHeight: '100vh', padding: '2rem' }}>
      <h2 style={{ color: '#e94560', textAlign: 'center', marginBottom: '2rem' }}>My Bookings</h2>
      <div style={{ maxWidth: '800px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {bookings.map(booking => (
          <div key={booking.id} style={{ backgroundColor: '#1a1a2e', border: '1px solid #333', borderRadius: '12px', padding: '1.5rem', color: '#ffffff' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
              <h3 style={{ color: '#e94560', margin: 0 }}>Booking #{booking.id}</h3>
              <span style={{ backgroundColor: '#ff9800', color: '#fff', padding: '0.25rem 0.75rem', borderRadius: '20px', fontSize: '0.85rem' }}>
                {booking.status.toUpperCase()}
              </span>
            </div>
            <p style={{ color: '#aaaaaa' }}><strong style={{ color: '#fff' }}>Name:</strong> {booking.customer_name}</p>
            <p style={{ color: '#aaaaaa' }}><strong style={{ color: '#fff' }}>Phone:</strong> {booking.phone_number}</p>
            <p style={{ color: '#aaaaaa' }}><strong style={{ color: '#fff' }}>Address:</strong> {booking.address}</p>
            <p style={{ color: '#aaaaaa' }}><strong style={{ color: '#fff' }}>Time:</strong> {booking.preferred_time}</p>
            <p style={{ color: '#aaaaaa' }}><strong style={{ color: '#fff' }}>Booked:</strong> {new Date(booking.created_at).toLocaleDateString()}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Bookings
