var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';
let HeaderCustom = class HeaderCustom extends LitElement {
    constructor() {
        super(...arguments);
        this.menuOpen = false;
    }
    static { this.styles = css `
    :host {
      display: block;
    }

    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background-color: #333;
      color: #fff;
    }

    nav {
      display: none;
    }

    .menu-icon {
      cursor: pointer;
      display: block;
      position: relative;
      width: 30px;
      height: 24px;
      transform: rotate(0deg);
      transition: 0.5s ease-in-out;
    }

    .menu-icon span {
      display: block;
      position: absolute;
      height: 3px;
      width: 100%;
      background-color: #fff;
      border-radius: 9px;
      opacity: 1;
      left: 0;
      transform: rotate(0deg);
      transition: 0.25s ease-in-out;
    }

    .menu-icon span:nth-child(1) {
      top: 0px;
    }

    .menu-icon span:nth-child(2) {
      top: 10px;
    }

    .menu-icon span:nth-child(3) {
      top: 20px;
    }

    .menu-icon.open span:nth-child(1) {
      top: 10px;
      transform: rotate(135deg);
    }

    .menu-icon.open span:nth-child(2) {
      opacity: 0;
      left: -60px;
    }

    .menu-icon.open span:nth-child(3) {
      top: 10px;
      transform: rotate(-135deg);
    }

    @media (min-width: 600px) {
      nav {
        display: flex;
      }

      .menu-icon {
        display: none;
      }
    }

    .active {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
  `; }
    toggleMenu() {
        this.menuOpen = !this.menuOpen;
    }
    render() {
        return html `
      <header>
        <div class="logo">My Logo</div>
        <nav class="${this.menuOpen ? 'active' : ''}">
          <a href="#">Home</a>
          <a href="#">About</a>
          <a href="#">Services</a>
          <a href="#">Contact</a>
        </nav>
        <div class="menu-icon ${this.menuOpen ? 'open' : ''}" @click="${this.toggleMenu}">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </header>
    `;
    }
};
__decorate([
    property({ type: Boolean })
], HeaderCustom.prototype, "menuOpen", void 0);
HeaderCustom = __decorate([
    customElement('header-custom')
], HeaderCustom);
export { HeaderCustom };
//# sourceMappingURL=header.js.map