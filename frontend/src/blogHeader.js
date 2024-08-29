var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';
let BlogHeader = class BlogHeader extends LitElement {
    constructor() {
        super(...arguments);
        this.menuOpen = true;
    }
    toggleMenu() {
        this.menuOpen = !this.menuOpen;
    }
    static { this.styles = css `
    .container {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px 0 15px;
      box-shadow: 0px 1px 10px #acacac;
    }
    
    .navbar-container-open {
      flex-direction: column;
      align-items: start;
    }

    .logo a {
      text-decoration: none;
      color: #3d3d3d;
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

    .menu-items-hide {
      display: none;
    }

    .menu-items-show {
      width: 100%;
    }

    .menu-items-show > menu {
      flex-direction: column;
    }

    .menu-items-show li {
      justify-content: space-around;
      display: flex;
      padding: 15px 0px;
      box-shadow: rgba(0, 0, 0, 0.05) 0px 2px 2px 0px;
    }

    .menu-items-show menu {
      padding-left: 0px;
    }

    .menu-items-show menu:first-child {
      margin-top: 0px;
    }

    .menu-items-show li > a {
      text-decoration: none;
      color: #3d3d3d;
    }
  `; }
    render() {
        return html `
      <header>
        <nav class="navbar">
          <div class="container ${this.menuOpen ? 'navbar-container-open' : ''}">
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
            <div class="menu-items ${this.menuOpen ? 'menu-items-show' : 'menu-items-hide'}">
              <menu>
              <li><a href="#">Home</a></li>
              <li><a href="#">blogs</a></li>
              <li><a href="#">portfolio</a></li>
              <li><a href="#">about</a></li>
              <li><a href="#">contact</a></li>
              </menu>
            </div>
          </div>
        </nav>
      </header>
    `;
    }
};
__decorate([
    property({ type: Boolean })
], BlogHeader.prototype, "menuOpen", void 0);
BlogHeader = __decorate([
    customElement('blog-header')
], BlogHeader);
//# sourceMappingURL=blogHeader.js.map