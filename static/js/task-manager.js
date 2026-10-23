// static/js/task-manager.js

// Task Manager Functions
const TaskManager = {
    // Toggle star status
    toggleStar: function(taskId) {
        fetch(`/toggle_star/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error toggling star:', error);
            location.reload();
        });
    },

    // Toggle pending/completed status
    togglePending: function(taskId) {
        fetch(`/toggle_pending/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error toggling pending:', error);
            location.reload();
        });
    },

    // Open color picker modal
    changeColor: function(taskId) {
        const colors = ['#000000', '#e63939', '#0077b6', '#2a9d8f', '#f4a261', '#9d4edd', '#e76f51', '#264653'];

        // Remove existing modal if present
        const existingModal = document.getElementById('colorModal');
        if (existingModal) {
            existingModal.remove();
        }

        // Create modal HTML
        const modalHTML = `
            <div class="modal fade" id="colorModal" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered modal-sm">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Choose Color</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="d-flex flex-wrap justify-content-center gap-2">
                                ${colors.map(color => `
                                    <button onclick="TaskManager.setColor(${taskId}, '${color}')"
                                            class="btn rounded-circle color-option"
                                            style="background-color: ${color}; width: 50px; height: 50px; border: 3px solid ${color === '#000000' ? '#333' : '#dee2e6'};"
                                            title="${color}">
                                    </button>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;

        // Add modal to body
        document.body.insertAdjacentHTML('beforeend', modalHTML);

        // Show modal
        const modalElement = document.getElementById('colorModal');
        const modal = new bootstrap.Modal(modalElement);
        modal.show();

        // Remove modal from DOM when hidden
        modalElement.addEventListener('hidden.bs.modal', () => {
            modalElement.remove();
        });
    },

    // Set task color
    setColor: function(taskId, color) {
        fetch(`/set_color/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ color: color })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error setting color:', error);
            location.reload();
        });
    },

    // Edit due date
    editDueDate: function(taskId, currentDate) {
        const newDate = prompt(
            "Enter due date & time (e.g., May 30, 3:00 PM):",
            currentDate
        );

        if (newDate !== null) {
            fetch(`/set_due_date/${taskId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ date: newDate })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            })
            .catch(error => {
                console.error('Error setting due date:', error);
                location.reload();
            });
        }
    },

    // Initialize
    init: function() {
        console.log('Task Manager initialized');
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    TaskManager.init();
});

// Make TaskManager globally accessible
window.TaskManager = TaskManager;