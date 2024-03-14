class ButtonMobile {
    constructor() {
        this.button = buttonElement();
    }
    
    openButton() {
        this.button.classList.add("active");
    }
    
    closeButton() {
        this.button.classlist.remove("active")
    }
    
    // Getter
    get buttonElement() {
        return document.querySelector(".button-menu-mobile");
    }
}