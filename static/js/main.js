/**
 * M-CLEAN — Premium Cleaning Website
 * Vanilla JS (No jQuery)
 */

document.addEventListener('DOMContentLoaded', () => {
    // ═══════════════════════════════════════════════════════════════
    // STICKY HEADER
    // ═══════════════════════════════════════════════════════════════
    const header = document.querySelector('.header');
    
    const handleScroll = () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };
    
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();

    // ═══════════════════════════════════════════════════════════════
    // MOBILE MENU TOGGLE
    // ═══════════════════════════════════════════════════════════════
    const mobileToggle = document.querySelector('.header__mobile-toggle');
    const headerNav = document.querySelector('.header__nav');

    if (mobileToggle && headerNav) {
        mobileToggle.addEventListener('click', () => {
            headerNav.classList.toggle('active');
            mobileToggle.classList.toggle('active');
        });

        // Close mobile menu on link click
        headerNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', (e) => {
                // If it's a dropdown button, let the other click handler manage the accordion
                if (!link.classList.contains('mobile-dropdown-btn')) {
                    headerNav.classList.remove('active');
                    mobileToggle.classList.remove('active');
                }
            });
        });
    }

    // ═══════════════════════════════════════════════════════════════
    // SCROLL ANIMATIONS (Intersection Observer)
    // ═══════════════════════════════════════════════════════════════
    const animateOnScroll = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                animateOnScroll.unobserve(entry.target);
            }
        });
    }, {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    });

    document.querySelectorAll('.fade-in, .slide-up, .slide-left, .section__title').forEach(el => {
        animateOnScroll.observe(el);
    });

    // ═══════════════════════════════════════════════════════════════
    // MODAL
    // ═══════════════════════════════════════════════════════════════
    const modalOverlay = document.querySelector('.modal-overlay');
    const modalClose = document.querySelector('.modal__close');
    const openModalBtns = document.querySelectorAll('[data-modal]');
    const leadForm = document.getElementById('lead-form');
    const leadSuccess = document.getElementById('lead-success');
    const leadFormWrap = document.getElementById('lead-form-wrap');
    const calcSummary = document.getElementById('calc-summary');

    const openModal = (modalId) => {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    };

    const closeModal = () => {
        if (modalOverlay) {
            modalOverlay.classList.remove('active');
            document.body.style.overflow = '';
            
            // Reset form after close
            setTimeout(() => {
                if (leadForm) leadForm.reset();
                if (leadSuccess) leadSuccess.style.display = 'none';
                if (leadFormWrap) leadFormWrap.style.display = 'block';
                if (calcSummary) calcSummary.style.display = 'none';
            }, 300);
        }
    };

    openModalBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const modalId = btn.dataset.modal || 'modal-lead';
            
            // If button has data-service-name and data-total-price, fill hidden fields
            const svcName = btn.dataset.serviceName || '';
            const totalPrice = btn.dataset.totalPrice || '';
            const optionsText = btn.dataset.options || '';
            const discountInfo = btn.dataset.discountInfo || '';
            if (svcName || totalPrice) {
                const snInput = document.getElementById('lead-service-name');
                const tpInput = document.getElementById('lead-total-price');
                const opInput = document.getElementById('lead-options');
                const diInput = document.getElementById('lead-discount-info');
                if (snInput) snInput.value = svcName;
                if (tpInput) tpInput.value = totalPrice;
                if (opInput) opInput.value = optionsText;
                if (diInput) diInput.value = discountInfo;
                
                // Show summary box
                if (calcSummary) {
                    const summarySvc = document.getElementById('calc-summary-service');
                    const summaryPrice = document.getElementById('calc-summary-price');
                    const summaryOpts = document.getElementById('calc-summary-options');
                    const summaryDiscounts = document.getElementById('calc-summary-discounts');
                    if (summarySvc) summarySvc.textContent = svcName;
                    // Don't add ₸ if it's already in the price
                    if (summaryPrice) {
                        summaryPrice.textContent = totalPrice.includes('₸') ? totalPrice : totalPrice + ' ₸';
                    }
                    if (summaryOpts) {
                        summaryOpts.textContent = optionsText;
                        summaryOpts.style.display = optionsText ? '' : 'none';
                    }
                    if (summaryDiscounts) {
                        summaryDiscounts.textContent = discountInfo;
                        summaryDiscounts.style.display = discountInfo ? '' : 'none';
                    }
                    calcSummary.style.display = 'block';
                }
            }
            
            openModal(modalId);
        });
    });

    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }

    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                closeModal();
            }
        });
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modalOverlay?.classList.contains('active')) {
            closeModal();
        }
    });

    // ═══════════════════════════════════════════════════════════════
    // LEAD FORM SUBMIT (AJAX)
    // ═══════════════════════════════════════════════════════════════
    if (leadForm) {
        leadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(leadForm);
            const submitBtn = leadForm.querySelector('.form-submit');
            
            const data = {
                name: formData.get('name'),
                phone: formData.get('phone'),
                service_name: document.getElementById('lead-service-name')?.value || '',
                total_price: document.getElementById('lead-total-price')?.value || '',
                options: document.getElementById('lead-options')?.value || '',
                discount_info: document.getElementById('lead-discount-info')?.value || '',
                source_page: document.getElementById('lead-source-page')?.value || '',
            };

            submitBtn.disabled = true;
            submitBtn.textContent = 'Отправка...';

            try {
                const response = await fetch('/api/lead/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (result.success) {
                    leadFormWrap.style.display = 'none';
                    calcSummary.style.display = 'none';
                    leadSuccess.style.display = 'block';

                    // Confetti burst on success
                    if (typeof confetti === 'function') {
                        confetti({
                            particleCount: 100,
                            spread: 70,
                            origin: { y: 0.6 },
                            colors: ['#059669', '#0f766e', '#d1fae5', '#ffffff']
                        });
                    }

                    setTimeout(() => {
                        closeModal();
                        if (leadForm) leadForm.reset();
                    }, 2500);
                } else {
                    showFormError(leadForm, result.error || 'Ошибка отправки данных. Попробуйте еще раз.');
                }
            } catch (error) {
                console.error('Form submit error:', error);
                showFormError(leadForm, 'Ошибка соединения с сервером. Попробуйте позже.');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Отправить заявку';
            }
        });
    }

    // Helper to show inline errors instead of native alert()
    function showFormError(form, message) {
        // Remove existing error if any
        const existingAlert = form.querySelector('.form-alert-error');
        if (existingAlert) existingAlert.remove();
        
        const alertEl = document.createElement('div');
        alertEl.className = 'form-alert-error fade-in';
        alertEl.style.cssText = 'padding: 12px 16px; margin-bottom: 20px; border-radius: 8px; background: #fee2e2; color: #b91c1c; border: 1px solid #f87171; font-size: 14px; text-align: center;';
        alertEl.textContent = message;
        
        form.insertBefore(alertEl, form.firstChild);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertEl.parentElement) alertEl.remove();
        }, 5000);
    }

    function getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // ═══════════════════════════════════════════════════════════════
    // MEGA MENU (JS-based for reliable hover)
    // ═══════════════════════════════════════════════════════════════
    const megaWrappers = document.querySelectorAll('.mega-menu-wrapper');
    
    megaWrappers.forEach(wrapper => {
        const menu = wrapper.querySelector('.mega-menu');
        if (!menu) return;
        
        let hideTimeout = null;
        
        const showMenu = () => {
            clearTimeout(hideTimeout);
            menu.style.opacity = '1';
            menu.style.visibility = 'visible';
            menu.style.pointerEvents = 'auto';
        };
        
        const hideMenu = () => {
            hideTimeout = setTimeout(() => {
                menu.style.opacity = '0';
                menu.style.visibility = 'hidden';
                menu.style.pointerEvents = 'none';
            }, 150);
        };
        
        wrapper.addEventListener('mouseenter', showMenu);
        wrapper.addEventListener('mouseleave', hideMenu);
    });
    // ═══════════════════════════════════════════════════════════════
    const initSlider = (container, beforeClass, handleClass) => {
        const before = container.querySelector(beforeClass);
        const handle = container.querySelector(handleClass);
        
        if (!before || !handle) return;

        let isDragging = false;

        const updatePosition = (x) => {
            const rect = container.getBoundingClientRect();
            let percentage = ((x - rect.left) / rect.width) * 100;
            percentage = Math.max(0, Math.min(100, percentage));
            
            before.style.clipPath = `inset(0 ${100 - percentage}% 0 0)`;
            handle.style.left = `${percentage}%`;
        };

        const startDrag = (e) => {
            isDragging = true;
            container.style.cursor = 'ew-resizing';
        };

        const endDrag = () => {
            isDragging = false;
            container.style.cursor = 'ew-resize';
        };

        const drag = (e) => {
            if (!isDragging) return;
            e.preventDefault();
            const x = e.type.includes('touch') ? e.touches[0].clientX : e.clientX;
            updatePosition(x);
        };

        container.addEventListener('mousedown', startDrag);
        document.addEventListener('mouseup', endDrag);
        document.addEventListener('mousemove', drag);

        container.addEventListener('touchstart', startDrag, { passive: true });
        document.addEventListener('touchend', endDrag);
        document.addEventListener('touchmove', drag, { passive: false });

        container.addEventListener('click', (e) => {
            updatePosition(e.clientX);
        });
    };

    document.querySelectorAll('.ba-slider').forEach(slider => {
        initSlider(slider, '.ba-slider__before', '.ba-slider__handle');
    });

    document.querySelectorAll('.portfolio-slider').forEach(slider => {
        initSlider(slider, '.portfolio-slider__before', '.portfolio-slider__line');
    });

    // ═══════════════════════════════════════════════════════════════
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ═══════════════════════════════════════════════════════════════
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ═══════════════════════════════════════════════════════════════
    // PHONE INPUT MASK (Simple)
    // ═══════════════════════════════════════════════════════════════
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    
    phoneInputs.forEach(input => {
        input.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 0) {
                if (value.length <= 1) {
                    value = '+' + value;
                } else if (value.length <= 4) {
                    value = '+' + value.substring(0,1) + ' (' + value.substring(1);
                } else if (value.length <= 7) {
                    value = '+' + value.substring(0,1) + ' (' + value.substring(1,4) + ') ' + value.substring(4);
                } else if (value.length <= 9) {
                    value = '+' + value.substring(0,1) + ' (' + value.substring(1,4) + ') ' + value.substring(4,7) + '-' + value.substring(7);
                } else {
                    value = '+' + value.substring(0,1) + ' (' + value.substring(1,4) + ') ' + value.substring(4,7) + '-' + value.substring(7,9) + '-' + value.substring(9,11);
                }
            }
            
            e.target.value = value;
        });
    });

    // ═══════════════════════════════════════════════════════════════
    // PARTNERS SWIPER (Infinite Autoplay)
    // ═══════════════════════════════════════════════════════════════
    if (typeof Swiper !== 'undefined') {
        const partnersSwiper = new Swiper('.partners-swiper', {
            slidesPerView: 2,
            spaceBetween: 20,
            loop: true,
            freeMode: {
                enabled: true,
                sticky: false,
            },
            autoplay: {
                delay: 1,
                disableOnInteraction: false,
                pauseOnMouseEnter: false,
            },
            speed: 4000,
            breakpoints: {
                640: {
                    slidesPerView: 3,
                    spaceBetween: 24,
                },
                1024: {
                    slidesPerView: 5,
                    spaceBetween: 30,
                },
            },
        });
    }
});
