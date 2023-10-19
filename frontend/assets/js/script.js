import React, { useState } from 'react';

function App() {
  // State variables for modal and notification toast
  const [isModalClosed, setModalClosed] = useState(true);
  const [isToastClosed, setToastClosed] = useState(true);

  // State variable for mobile menu and overlay
  const [isMobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Event handler for closing the modal
  const closeModal = () => {
    setModalClosed(true);
  };

  // Event handler for closing the notification toast
  const closeToast = () => {
    setToastClosed(true);
  };

  // Event handler for opening/closing the mobile menu
  const toggleMobileMenu = () => {
    setMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <div>
      {/* Modal */}
      <div className={`modal ${isModalClosed ? 'closed' : ''}`}>
        {/* Modal content */}
        <button onClick={closeModal}>Close Modal</button>
      </div>

      {/* Notification Toast */}
      <div className={`notification-toast ${isToastClosed ? 'closed' : ''}`}>
        {/* Toast content */}
        <button onClick={closeToast}>Close Toast</button>
      </div>

      {/* Mobile Menu */}
      <button onClick={toggleMobileMenu}>Toggle Mobile Menu</button>
      {isMobileMenuOpen && (
        <div className="mobile-menu">
          {/* Mobile menu content */}
          <button onClick={toggleMobileMenu}>Close Mobile Menu</button>
        </div>
      )}

      {/* Overlay */}
      {isMobileMenuOpen && <div className="overlay" onClick={toggleMobileMenu}></div>}
    </div>
  );
}

export default App;
