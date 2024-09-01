import {LitElement, html, css} from 'lit';
import {customElement, property} from 'lit/decorators.js';

@customElement('blog-header')
class BlogHeader extends LitElement {
  @property({type: Boolean})
  menuOpen = true;

  /** Sizes  */
  @property({type: Number})
  smallWidth = 600;

  toggleMenu() {
    this.menuOpen = !this.menuOpen;
  }

  @property({type: Number}) windowWidth: number = window.innerWidth;

  private updateWindowSize() {
    this.windowWidth = window.innerWidth;

    /** Close the hamburger menu if it is not shown */
    if (this.windowWidth >= this.smallWidth) {
      this.menuOpen = false;
    }
  }

  override connectedCallback() {
    super.connectedCallback();
    // Ajouter un écouteur d'événements pour détecter la redimension de la fenêtre
    window.addEventListener('resize', this.updateWindowSize.bind(this));
  }

  override disconnectedCallback() {
    super.disconnectedCallback();
    // Retirer l'écouteur d'événements lorsque le composant est retiré du DOM
    window.removeEventListener('resize', this.updateWindowSize.bind(this));
  }

  static override styles = css`
    .container {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 0px 0px 0px;
      box-shadow: 0px 1px 10px #acacac;
    }

    .navbar-container-open {
      flex-direction: column;
      align-items: start;
    }

    .logo a {
      text-decoration: none;
      color: #3d3d3d;
      margin-left: 20px;
    }

    .hamburger-lines {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-evenly;
      height: 25px;
      width: 25px;
      border: 1px solid #949494;
      box-shadow: 1px 1px 3px #acacac;
      border-radius: 3px;
      margin-right: 20px;
    }

    .hamburger-lines:hover {
      cursor: pointer;
    }

    .hamburger-lines:active {
      box-shadow: -1px -1px 3px #acacac;
    }

    .hamburger-lines .hamburger-line {
      width: 65%;
      height: 3px;
      border-radius: 2px;
      background-color: #000000;
      transition: 0.25s ease-in-out;
    }

    .hamburger-lines.active {
      position: absolute;
      top: 23px;
      right: 20px;
      margin-right: 0px;
    }

    .active .hamburger-line1 {
      transform: rotate(45deg) translate(5px, 5px);
    }

    .active .hamburger-line2 {
      transform: scaleY(0);
    }

    .active .hamburger-line3 {
      transform: rotate(-45deg) translate(5px, -5px);
    }

    .menu-items {
      display: none;
    }

    .menu-items-show {
      display: block;
      width: 100%;
      flex-direction: column;
      box-shadow: rgba(0, 0, 0, 0.05) 0px -2px 2px 0px;
      padding-left: 0px;
    }

    .menu-items-show li {
      justify-content: space-around;
      display: flex;
      padding: 15px 0px;
      box-shadow: rgba(0, 0, 0, 0.05) 0px 2px 2px 0px;
    }

    .menu-items-show:first-child {
      margin-top: 0px;
    }

    .menu-items-show li > a {
      text-decoration: none;
      color: #3d3d3d;
    }

    @media screen and (min-width: 600px) {
      .hamburger-lines {
        display: none;
      }

      .menu-items {
        display: flex;
        align-self: stretch;
        padding-left: 0px;
        margin: 0px 0px;
        box-shadow: rgba(0, 0, 0, 0.05) -2px 0px 2px 0px;
      }

      .menu-items > li {
        display: flex;
        list-style-type: none;
        border: none;
        box-shadow: rgba(0, 0, 0, 0.05) 2px 0px 2px 0px;
        padding: 0px 12px;
        align-items: center;
      }

      .menu-items li > a {
        text-decoration: none;
        color: #3d3d3d;
      }
    }
  `;

  override render() {
    return html`
      <header>
        <nav
          class="navbar container ${this.menuOpen
            ? 'navbar-container-open'
            : ''}"
        >
          <div class="logo">
            <h1><a href="#">Mon Blog</a></h1>
          </div>
          <div
            class="hamburger-lines 
              ${this.menuOpen ? 'active' : ''}"
            @click="${this.toggleMenu}"
          >
            <span class="hamburger-line hamburger-line1"></span>
            <span class="hamburger-line hamburger-line2"></span>
            <span class="hamburger-line hamburger-line3"></span>
          </div>
          <menu class="menu-items ${this.menuOpen ? 'menu-items-show' : ''}">
            <li><a href="#">Home</a></li>
            <li><a href="#">blogs</a></li>
            <li><a href="#">portfolio</a></li>
            <li><a href="#">about</a></li>
            <li><a href="#">contact</a></li>
          </menu>
        </nav>
      </header>
    `;
  }
}
