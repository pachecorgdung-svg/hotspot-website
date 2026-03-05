// 跨境电商热点追踪系统 - 主JavaScript文件

document.addEventListener('DOMContentLoaded', function() {
    console.log('跨境电商热点追踪系统已加载');

    // 初始化工具提示
    initTooltips();

    // 初始化卡片动画
    initCardAnimations();

    // 初始化刷新按钮
    initRefreshButton();

    // 检查数据更新
    checkDataFreshness();
});

// 工具提示初始化
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const tooltipText = this.getAttribute('data-tooltip');
            if (!tooltipText) return;

            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = tooltipText;
            document.body.appendChild(tooltip);

            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';

            this._tooltip = tooltip;
        });

        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
}

// 卡片动画初始化
function initCardAnimations() {
    const cards = document.querySelectorAll('.hotspot-card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
}

// 刷新按钮初始化
function initRefreshButton() {
    const refreshBtn = document.querySelector('.btn-refresh');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function(e) {
            e.preventDefault();
            refreshData();
        });
    }
}

// 刷新数据
function refreshData() {
    const btn = document.querySelector('.btn-refresh');
    if (!btn) return;

    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 更新中...';
    btn.disabled = true;

    // 显示加载状态
    showLoadingOverlay();

    fetch('/api/hotspots/update', {
        method: 'POST',
        headers: {
            'X-Auth-Token': 'your-admin-token-change-this'  // 实际应用中应从安全位置获取
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('数据更新任务已启动，请稍后刷新页面查看最新热点', 'success');

            // 延迟刷新页面
            setTimeout(() => {
                location.reload();
            }, 3000);
        } else {
            showNotification('更新失败: ' + (data.error || '未知错误'), 'error');
            resetButton(btn, originalText);
        }
    })
    .catch(error => {
        console.error('刷新失败:', error);
        showNotification('网络错误，请检查连接', 'error');
        resetButton(btn, originalText);
    })
    .finally(() => {
        hideLoadingOverlay();
    });
}

// 显示加载遮罩
function showLoadingOverlay() {
    let overlay = document.getElementById('loading-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        `;

        const spinner = document.createElement('div');
        spinner.style.cssText = `
            border: 4px solid #f3f3f3;
            border-top: 4px solid #4a6cf7;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
        `;

        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;

        document.head.appendChild(style);
        overlay.appendChild(spinner);
        document.body.appendChild(overlay);
    }

    overlay.style.display = 'flex';
}

// 隐藏加载遮罩
function hideLoadingOverlay() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

// 重置按钮状态
function resetButton(btn, originalText) {
    btn.innerHTML = originalText;
    btn.disabled = false;
}

// 显示通知
function showNotification(message, type = 'info') {
    // 移除旧的通知
    const oldNotification = document.querySelector('.custom-notification');
    if (oldNotification) {
        oldNotification.remove();
    }

    const notification = document.createElement('div');
    notification.className = `custom-notification ${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#51cf66' : type === 'error' ? '#ff6b6b' : '#4a6cf7'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        max-width: 400px;
        word-wrap: break-word;
    `;

    notification.textContent = message;
    document.body.appendChild(notification);

    // 自动消失
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);

    // 添加动画样式
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
}

// 检查数据新鲜度
function checkDataFreshness() {
    const lastUpdateElement = document.querySelector('.stat-item span');
    if (!lastUpdateElement) return;

    const lastUpdateText = lastUpdateElement.textContent;
    const updateMatch = lastUpdateText.match(/\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/);

    if (updateMatch) {
        const lastUpdate = new Date(updateMatch[0]);
        const now = new Date();
        const hoursDiff = (now - lastUpdate) / (1000 * 60 * 60);

        if (hoursDiff > 24) {
            showNotification('数据已超过24小时未更新，建议手动刷新', 'warning');
        }
    }
}

// 分享热点
function shareHotspot(hotspotId) {
    const hotspotElement = document.querySelector(`.hotspot-card:nth-child(${hotspotId})`);
    if (!hotspotElement) return;

    const title = hotspotElement.querySelector('.card-title')?.textContent || '跨境电商热点';
    const url = window.location.href;

    const shareData = {
        title: '跨境电商热点追踪',
        text: `热点推荐: ${title}`,
        url: url
    };

    if (navigator.share) {
        navigator.share(shareData)
            .then(() => console.log('分享成功'))
            .catch(error => console.log('分享取消:', error));
    } else {
        // 降级方案：复制到剪贴板
        const textToCopy = `${title}\n${url}`;
        navigator.clipboard.writeText(textToCopy)
            .then(() => showNotification('热点链接已复制到剪贴板', 'success'))
            .catch(err => showNotification('复制失败，请手动复制', 'error'));
    }
}

// 搜索功能（如果需要）
function initSearch() {
    const searchInput = document.createElement('input');
    searchInput.type = 'search';
    searchInput.placeholder = '搜索热点...';
    searchInput.className = 'search-input';

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const cards = document.querySelectorAll('.hotspot-card');

        cards.forEach(card => {
            const title = card.querySelector('.card-title').textContent.toLowerCase();
            const summary = card.querySelector('.card-summary').textContent.toLowerCase();
            const tags = card.querySelector('.card-tags')?.textContent.toLowerCase() || '';

            const isVisible = title.includes(searchTerm) ||
                            summary.includes(searchTerm) ||
                            tags.includes(searchTerm);

            card.style.display = isVisible ? 'flex' : 'none';
        });
    });

    // 将搜索框添加到页面
    const header = document.querySelector('.page-header');
    if (header) {
        header.appendChild(searchInput);
    }
}

// 导出功能（如果需要）
function exportData(format = 'json') {
    fetch('/api/hotspots/today')
        .then(response => response.json())
        .then(data => {
            if (format === 'json') {
                const jsonStr = JSON.stringify(data, null, 2);
                downloadFile(jsonStr, 'hotspots.json', 'application/json');
            } else if (format === 'csv') {
                // 简化的CSV转换
                const csv = convertToCSV(data.data);
                downloadFile(csv, 'hotspots.csv', 'text/csv');
            }
        })
        .catch(error => {
            console.error('导出失败:', error);
            showNotification('导出失败', 'error');
        });
}

function convertToCSV(data) {
    if (!data || data.length === 0) return '';

    const headers = ['排名', '标题', '来源', '热度', '发布时间'];
    const rows = data.map((item, index) => [
        index + 1,
        `"${item.title.replace(/"/g, '""')}"`,
        item.source_site,
        item.heat_score,
        item.publish_date
    ]);

    return [headers, ...rows].map(row => row.join(',')).join('\n');
}

function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// 添加到全局对象，以便模板中可以调用
window.refreshData = refreshData;
window.shareHotspot = shareHotspot;
window.exportData = exportData;