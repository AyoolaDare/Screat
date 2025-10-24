class CustomNavbar extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <style>
        nav {
          background: white;
          padding: 1rem 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
          position: sticky;
          top: 0;
          z-index: 50;
        }
        .logo img {
          height: 40px;
        }
ul {
          display: flex;
          gap: 2rem;
          list-style: none;
          margin: 0;
          padding: 0;
          align-items: center;
        }
        a {
          color: #4b5563;
          text-decoration: none;
          font-weight: 500;
          transition: color 0.2s;
          display: flex;
          align-items: center;
          gap: 0.25rem;
        }
        a:hover {
          color: #4f46e5;
        }
        .apply-btn {
          background: #4f46e5;
          color: white;
          padding: 0.5rem 1.5rem;
          border-radius: 9999px;
          transition: background 0.2s;
        }
        .apply-btn:hover {
          background: #4338ca;
          color: white;
        }
        .mobile-menu-btn {
          display: none;
          background: none;
          border: none;
          color: #4b5563;
          cursor: pointer;
        }
        @media (max-width: 768px) {
          ul {
            display: none;
          }
          .mobile-menu-btn {
            display: block;
          }
          nav {
            padding: 1rem;
          }
        }
      </style>
      <nav>
        <div class="logo">
          <img src="https://huggingface.co/spaces/Ayostag/undercover-shopping-spree/resolve/main/images/Screen Shot 2025-10-10 at 3_33_15 PM.avif" alt="Secret Shopper Express Logo" class="h-10">
</div>
<button class="mobile-menu-btn">
          <i data-feather="menu"></i>
        </button>
        
        <ul>
          <li><a href="/"><i data-feather="home" width="18"></i> Home</a></li>
          <li><a href="#"><i data-feather="info" width="18"></i> About</a></li>
          <li><a href="#"><i data-feather="dollar-sign" width="18"></i> Earnings</a></li>
          <li><a href="#"><i data-feather="shopping-bag" width="18"></i> Assignments</a></li>
          <li><a href="/contact.html"><i data-feather="mail" width="18"></i> Contact</a></li>
<li><a href="#apply" class="apply-btn">Apply Now</a></li>
        </ul>
      </nav>
    `;

    // Mobile menu functionality
    const mobileMenuBtn = this.shadowRoot.querySelector('.mobile-menu-btn');
    const menu = this.shadowRoot.querySelector('ul');
    
    if(mobileMenuBtn) {
      mobileMenuBtn.addEventListener('click', () => {
        menu.style.display = menu.style.display === 'flex' ? 'none' : 'flex';
      });
    }
  }
}

customElements.define('custom-navbar', CustomNavbar);