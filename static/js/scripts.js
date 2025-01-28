// Function to handle file upload and display a success message
document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let formData = new FormData(this);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('success', 'Files uploaded successfully!');
            window.location.href = "/dashboard"; // Redirect to dashboard after successful upload
        } else {
            showAlert('danger', 'There was an error uploading the files. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error uploading files:', error);
        showAlert('danger', 'There was an error uploading the files. Please try again.');
    });
});

// Function to show alert messages
function showAlert(type, message) {
    let alertBox = document.createElement('div');
    alertBox.classList.add('alert', type);
    alertBox.textContent = message;

    document.body.appendChild(alertBox);
    
    setTimeout(() => {
        alertBox.remove();
    }, 3000);
}

// Function to display the matching score in the dashboard
function displayMatchingScores(cvData) {
    let resultContainer = document.getElementById("matchingScores");
    resultContainer.innerHTML = '';

    cvData.forEach(cv => {
        let resultItem = document.createElement('div');
        resultItem.classList.add('dashboard-item');
        resultItem.innerHTML = `
            <h3>${cv.filename}</h3>
            <p>Matching Score: ${cv.matching_score}</p>
            <button onclick="viewDetails(${cv.id})">View Details</button>
        `;
        resultContainer.appendChild(resultItem);
    });
}

// Function to view detailed matching results for a specific CV
function viewDetails(cvId) {
    fetch(`/cv/details/${cvId}`)
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayDetailedStats(data.cvDetails);
        } else {
            showAlert('danger', 'Failed to load CV details.');
        }
    })
    .catch(error => {
        console.error('Error fetching CV details:', error);
        showAlert('danger', 'Failed to load CV details.');
    });
}

// Function to display detailed CV matching stats in a modal or section
function displayDetailedStats(cvDetails) {
    let modalContent = document.getElementById("cvDetailsModalContent");
    modalContent.innerHTML = `
        <h4>Details for ${cvDetails.filename}</h4>
        <p>Matching Score: ${cvDetails.matching_score}</p>
        <p>Keywords Matched: ${cvDetails.keywords}</p>
        <p>Similarity Score: ${cvDetails.similarity_score}</p>
    `;
    document.getElementById("cvDetailsModal").style.display = "block"; // Open modal
}

// Function to close the modal displaying CV details
function closeModal() {
    document.getElementById("cvDetailsModal").style.display = "none"; // Close modal
}

// Event listener to close modal when user clicks outside the modal
window.onclick = function(event) {
    if (event.target === document.getElementById("cvDetailsModal")) {
        closeModal();
    }
};

// Function to handle CRUD operations for CV and JD management
function deleteFile(fileId, type) {
    if (confirm("Are you sure you want to delete this file?")) {
        fetch(`/delete/${type}/${fileId}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('success', `${type.toUpperCase()} deleted successfully!`);
                window.location.reload(); // Reload page to reflect changes
            } else {
                showAlert('danger', `Failed to delete ${type.toUpperCase()}.`);
            }
        })
        .catch(error => {
            console.error('Error deleting file:', error);
            showAlert('danger', `Failed to delete ${type.toUpperCase()}.`);
        });
    }
}

function renameFile(fileId, type) {
    let newName = prompt("Enter a new name for the file:");
    if (newName) {
        fetch(`/rename/${type}/${fileId}`, {
            method: 'PUT',
            body: JSON.stringify({ newName: newName }),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('success', `${type.toUpperCase()} renamed successfully!`);
                window.location.reload();
            } else {
                showAlert('danger', `Failed to rename ${type.toUpperCase()}.`);
            }
        })
        .catch(error => {
            console.error('Error renaming file:', error);
            showAlert('danger', `Failed to rename ${type.toUpperCase()}.`);
        });
    }
}
