var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
import { LitElement, html, css } from 'lit';
import { customElement } from 'lit/decorators.js';
let FooterCustom = class FooterCustom extends LitElement {
    static { this.styles = css `
    /* Footer styling */
    footer-custom {
      background-color: #2c3e50;
      color: white;
      padding: 20px 0;
      text-align: center;
    }

    .footer-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      max-width: 1000px;
      margin: 0 auto;
    }

    .footer-section {
      margin-bottom: 20px;
      width: 100%;
      padding: 10px;
    }

    .footer-section h2 {
      font-size: 18px;
      margin-bottom: 10px;
    }

    .footer-section p,
    .footer-section ul {
      font-size: 14px;
      margin: 0;
      padding: 0;
      list-style-type: none;
    }

    .footer-section ul li {
      margin-bottom: 10px;
    }

    .footer-section ul li a {
      color: white;
      text-decoration: none;
    }

    .footer-section ul li a:hover {
      text-decoration: underline;
    }

    .social-links a {
      margin: 0 10px;
      display: inline-block;
    }

    .social-links img {
      width: 24px;
      height: 24px;
    }

    .footer-bottom {
      padding-top: 20px;
      border-top: 1px solid #ffffff33;
      font-size: 12px;
    }

    /* Desktop view */
    @media (min-width: 768px) {
      .footer-content {
        flex-direction: row;
        justify-content: space-between;
        text-align: left;
      }

      .footer-section {
        width: 30%;
      }

      .footer-bottom {
        text-align: center;
      }
    }
  `; }
    render() {
        return html `
      <div class="footer-content">
        <div class="footer-section about">
          <h2>À propos</h2>
          <p>Texte court sur votre site ou votre entreprise.</p>
        </div>
        <div class="footer-section links">
          <h2>Liens rapides</h2>
          <ul>
            <li><a href="#">Accueil</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">À propos</a></li>
            <li><a href="#">Contact</a></li>
          </ul>
        </div>
        <div class="footer-section social">
          <h2>Suivez-nous</h2>
          <div class="social-links">
            <a href="#"><img src="icon-facebook.png" alt="Facebook" /></a>
            <a href="#"><img src="icon-twitter.png" alt="Twitter" /></a>
            <a href="#"><img src="icon-instagram.png" alt="Instagram" /></a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        &copy; 2024 MonBlog | Tous droits réservés
      </div>
    `;
    }
};
FooterCustom = __decorate([
    customElement('footer-custom')
], FooterCustom);
export { FooterCustom };
//# sourceMappingURL=footer.js.map