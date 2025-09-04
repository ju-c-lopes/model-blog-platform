// Post Editor - Rich Text Editor with Quill.js
// Handles post creation and editing with WYSIWYG capabilities

class PostEditor {
    constructor() {
        this.quill = null;
        this.init();
    }

    init() {
        // Initialize Quill editor
        this.initQuillEditor();

        // Setup event listeners
        this.setupEventListeners();

        // Setup character counters
        this.setupCharacterCounters();

        // Setup form validation
        this.setupFormValidation();
    }

    initQuillEditor() {
        // Custom toolbar configuration
        const toolbarOptions = [
            [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
            ['bold', 'italic', 'underline', 'strike'],
            [{ 'color': [] }, { 'background': [] }],
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
            [{ 'indent': '-1'}, { 'indent': '+1' }],
            [{ 'align': [] }],
            ['blockquote', 'code-block'],
            ['link', 'image', 'video'],
            ['clean']
        ];

        // Initialize Quill
        this.quill = new Quill('#editor-container', {
            theme: 'snow',
            modules: {
                toolbar: {
                    container: toolbarOptions,
                    handlers: {
                        'image': this.imageHandler.bind(this),
                        'video': this.videoHandler.bind(this)
                    }
                },
                table: true
            },
            placeholder: 'Write your post content here...'
        });

        // Sync Quill content with hidden textarea
        this.quill.on('text-change', () => {
            const content = this.quill.root.innerHTML;
            document.getElementById('id_text').value = content;
            this.updateWordCount();
        });
    }

    setupEventListeners() {
        // Add table button functionality
        const addTableBtn = document.getElementById('add-table-btn');
        if (addTableBtn) {
            addTableBtn.addEventListener('click', this.insertTable.bind(this));
        }

        // Form submission
        const form = document.getElementById('post-form');
        if (form) {
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        }

        // Auto-generate URL slug from title
        const titleField = document.getElementById('id_title');
        const slugField = document.getElementById('id_url_slug');

        if (titleField && slugField) {
            titleField.addEventListener('input', (e) => {
                if (!slugField.dataset.userModified) {
                    slugField.value = this.generateSlug(e.target.value);
                }
            });

            slugField.addEventListener('input', () => {
                slugField.dataset.userModified = 'true';
            });
        }
    }

    setupCharacterCounters() {
        // Title counter
        const titleField = document.getElementById('id_title');
        const titleCounter = document.getElementById('title-counter');

        if (titleField && titleCounter) {
            titleField.addEventListener('input', (e) => {
                const count = e.target.value.length;
                titleCounter.textContent = `${count}/100`;
                titleCounter.className = count > 100 ? 'char-counter error' : 'char-counter';
            });
        }

        // Meta description counter
        const metaField = document.getElementById('id_meta_description');
        const metaCounter = document.getElementById('meta-counter');

        if (metaField && metaCounter) {
            metaField.addEventListener('input', (e) => {
                const count = e.target.value.length;
                metaCounter.textContent = `${count}/160`;
                metaCounter.className = count > 160 ? 'char-counter error' : 'char-counter';
            });
        }
    }

    setupFormValidation() {
        const form = document.getElementById('post-form');
        if (!form) return;

        const inputs = form.querySelectorAll('input[required], textarea[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', this.validateField.bind(this));
            input.addEventListener('input', this.clearFieldError.bind(this));
        });
    }

    validateField(event) {
        const field = event.target;
        const value = field.value.trim();
        const fieldGroup = field.closest('.form-group');

        if (!fieldGroup) return;

        // Remove existing error
        this.clearFieldError(event);

        // Validate based on field type
        let isValid = true;
        let errorMessage = '';

        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'This field is required.';
        } else if (field.id === 'id_title' && value.length > 100) {
            isValid = false;
            errorMessage = 'Title must be 100 characters or less.';
        } else if (field.id === 'id_meta_description' && value.length > 160) {
            isValid = false;
            errorMessage = 'Meta description must be 160 characters or less.';
        }

        if (!isValid) {
            this.showFieldError(fieldGroup, errorMessage);
        }
    }

    clearFieldError(event) {
        const fieldGroup = event.target.closest('.form-group');
        if (fieldGroup) {
            const existingError = fieldGroup.querySelector('.field-error');
            if (existingError) {
                existingError.remove();
            }
            fieldGroup.classList.remove('error');
        }
    }

    showFieldError(fieldGroup, message) {
        fieldGroup.classList.add('error');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.textContent = message;
        fieldGroup.appendChild(errorDiv);
    }

    updateWordCount() {
        const wordCounter = document.getElementById('word-counter');
        if (wordCounter && this.quill) {
            const text = this.quill.getText();
            const wordCount = text.trim().split(/\s+/).filter(word => word.length > 0).length;
            wordCounter.textContent = `${wordCount} words`;
        }
    }

    generateSlug(title) {
        return title
            .toLowerCase()
            .trim()
            .replace(/[^\w\s-]/g, '') // Remove special characters
            .replace(/[\s_-]+/g, '-') // Replace spaces and underscores with hyphens
            .replace(/^-+|-+$/g, ''); // Remove leading/trailing hyphens
    }

    imageHandler() {
        const input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');
        input.click();

        input.onchange = () => {
            const file = input.files[0];
            if (file) {
                this.uploadImage(file);
            }
        };
    }

    videoHandler() {
        const url = prompt('Enter video URL (YouTube, Vimeo, etc.):');
        if (url) {
            const range = this.quill.getSelection();
            this.quill.insertEmbed(range.index, 'video', url);
        }
    }

    uploadImage(file) {
        // Create FormData for file upload
        const formData = new FormData();
        formData.append('image', file);
        formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

        // Show loading indicator
        this.showUploadProgress('Uploading image...');

        // Upload to server (you'll need to create this endpoint)
        fetch('/upload-image/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            this.hideUploadProgress();
            if (data.success) {
                const range = this.quill.getSelection();
                this.quill.insertEmbed(range.index, 'image', data.url);
            } else {
                alert('Failed to upload image: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            this.hideUploadProgress();
            console.error('Upload error:', error);
            alert('Failed to upload image. Please try again.');
        });
    }

    insertTable() {
        const rows = prompt('Number of rows:', '3');
        const cols = prompt('Number of columns:', '3');

        if (rows && cols) {
            const tableModule = this.quill.getModule('table');
            if (tableModule) {
                tableModule.insertTable(parseInt(rows), parseInt(cols));
            } else {
                // Fallback: insert HTML table
                this.insertHTMLTable(parseInt(rows), parseInt(cols));
            }
        }
    }

    insertHTMLTable(rows, cols) {
        let tableHTML = '<table class="table table-bordered"><tbody>';

        for (let i = 0; i < rows; i++) {
            tableHTML += '<tr>';
            for (let j = 0; j < cols; j++) {
                tableHTML += '<td>&nbsp;</td>';
            }
            tableHTML += '</tr>';
        }

        tableHTML += '</tbody></table>';

        const range = this.quill.getSelection();
        this.quill.clipboard.dangerouslyPasteHTML(range.index, tableHTML);
    }

    showUploadProgress(message) {
        const progressDiv = document.getElementById('upload-progress') || this.createProgressDiv();
        progressDiv.textContent = message;
        progressDiv.style.display = 'block';
    }

    hideUploadProgress() {
        const progressDiv = document.getElementById('upload-progress');
        if (progressDiv) {
            progressDiv.style.display = 'none';
        }
    }

    createProgressDiv() {
        const div = document.createElement('div');
        div.id = 'upload-progress';
        div.className = 'upload-progress';
        div.style.display = 'none';
        document.body.appendChild(div);
        return div;
    }

    handleFormSubmit(event) {
        // Ensure Quill content is synced
        if (this.quill) {
            const content = this.quill.root.innerHTML;
            document.getElementById('id_text').value = content;
        }

        // Validate form
        const form = event.target;
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                this.validateField({ target: field });
                isValid = false;
            }
        });

        if (!isValid) {
            event.preventDefault();
            alert('Please fill in all required fields.');
        }
    }
}

// Initialize editor when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if we're on the post creation/edit page
    if (document.getElementById('editor-container')) {
        new PostEditor();
    }
});

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PostEditor;
}
