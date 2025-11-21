const API_URL = 'http://localhost/api';

// Функция для отправки формы
document.getElementById('contractForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        title: document.getElementById('title').value,
        client: document.getElementById('client').value,
        start_date: document.getElementById('startDate').value,
        status: document.getElementById('status').value,
        description: document.getElementById('description').value
    };

    try {
        const response = await fetch(`${API_URL}/contracts/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        if (response.ok) {
            alert('✅ Контракт успешно добавлен!');
            document.getElementById('contractForm').reset();
            loadContracts();
        } else {
            const errorData = await response.json();
            alert(`❌ Ошибка: ${errorData.detail || 'Неизвестная ошибка'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('🔌 Сетевая ошибка. Проверьте подключение к бэкенду.');
    }
});

// Функция для загрузки и отображения контрактов
async function loadContracts() {
    try {
        const response = await fetch(`${API_URL}/contracts/`);
        if (!response.ok) throw new Error('Ошибка загрузки контрактов');
        
        const contracts = await response.json();
        
        const contractsList = document.getElementById('contractsList');
        const contractCount = document.getElementById('contractCount');
        
        contractCount.textContent = `Контрактов: ${contracts.length}`;
        contractsList.innerHTML = '';

        if (contracts.length === 0) {
            contractsList.innerHTML = '<p class="no-contracts">Контрактов пока нет</p>';
            return;
        }

        contracts.forEach(contract => {
            const contractElement = document.createElement('div');
            contractElement.className = 'contract-item';
            contractElement.innerHTML = `
                <div class="contract-header">
                    <strong>${contract.title}</strong>
                    <span class="contract-id">#${contract.id}</span>
                </div>
                <div class="contract-client">👤 Клиент: ${contract.client}</div>
                <div class="contract-date">📅 Дата начала: ${contract.start_date}</div>
                <div class="contract-status">🏷️ Статус: ${contract.status}</div>
                ${contract.description ? `<div class="contract-description">📝 ${contract.description}</div>` : ''}
                <button onclick="deleteContract(${contract.id})" class="delete-btn">🗑️ Удалить</button>
            `;
            contractsList.appendChild(contractElement);
        });
    } catch (error) {
        console.error('Error loading contracts:', error);
        document.getElementById('contractsList').innerHTML = 
            '<p class="error">❌ Ошибка загрузки контрактов</p>';
    }
}

// Функция для удаления контракта
async function deleteContract(contractId) {
    if (!confirm('Вы уверены, что хотите удалить этот контракт?')) return;
    
    try {
        const response = await fetch(`${API_URL}/contracts/${contractId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('✅ Контракт удален!');
            loadContracts();
        } else {
            alert('❌ Ошибка при удалении контракта');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('🔌 Сетевая ошибка');
    }
}

// Загружаем контракты при загрузке страницы
window.onload = loadContracts;