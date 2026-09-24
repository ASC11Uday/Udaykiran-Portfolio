import {
  AfterViewInit,
  Component,
  ElementRef,
  OnDestroy,
  ViewChild,
  signal
} from '@angular/core';

@Component({
  selector: 'app-navbar',
  imports: [],
  templateUrl: './navbar.html',
  styleUrl: './navbar.scss'
})
export class Navbar implements AfterViewInit, OnDestroy {

  @ViewChild('progressBar')
  progressBar!: ElementRef<HTMLElement>;

  isMenuOpen = false;

  activeSection = signal('home');

  private scrollHandler?: () => void;
  private resizeHandler?: () => void;
  private animationFrameId = 0;

  toggleMenu(): void {
    this.isMenuOpen = !this.isMenuOpen;
  }

  closeMenu(): void {
    this.isMenuOpen = false;
  }

  setActiveSection(section: string): void {
    this.activeSection.set(section);
    this.closeMenu();
  }

  ngAfterViewInit(): void {

    setTimeout(() => {
      this.updateScrollState();
    }, 100);

    this.scrollHandler = () => {

      if (this.animationFrameId) {
        return;
      }

      this.animationFrameId =
        requestAnimationFrame(() => {

          this.updateScrollState();

          this.animationFrameId = 0;
        });
    };

    this.resizeHandler = () => {
      this.updateScrollState();
    };

    window.addEventListener(
      'scroll',
      this.scrollHandler,
      { passive: true }
    );

    window.addEventListener(
      'resize',
      this.resizeHandler,
      { passive: true }
    );
  }

  private updateScrollState(): void {
    this.updateProgress();
    this.detectActiveSection();
  }

  /* =========================================
     PROGRESS LINE
  ========================================= */

  private updateProgress(): void {

    if (!this.progressBar) {
      return;
    }

    const scrollTop =
      window.scrollY;

    const documentHeight =
      document.documentElement.scrollHeight;

    const viewportHeight =
      window.innerHeight;

    const scrollableHeight =
      documentHeight - viewportHeight;

    if (scrollableHeight <= 0) {
      this.progressBar.nativeElement.style.width = '0%';
      return;
    }

    const progress =
      (scrollTop / scrollableHeight) * 100;

    this.progressBar.nativeElement.style.width =
      `${Math.min(100, Math.max(0, progress))}%`;
  }

  /* =========================================
     ACTIVE SECTION
  ========================================= */

  private detectActiveSection(): void {

    const sectionIds = [
      'home',
      'about',
      'experience',
      'projects',
      'skills',
      'contact'
    ];

    let currentSection = 'home';

    const navbar =
      document.querySelector('.navbar');

    const navbarHeight =
      navbar?.getBoundingClientRect().height ?? 70;

    const triggerPoint =
      navbarHeight + 80;

    for (const id of sectionIds) {

      const section =
        document.getElementById(id);

      if (!section) {
        continue;
      }

      const rect =
        section.getBoundingClientRect();

      if (rect.top <= triggerPoint) {
        currentSection = id;
      }
    }

    const reachedBottom =
      window.scrollY +
      window.innerHeight >=
      document.documentElement.scrollHeight - 5;

    if (reachedBottom) {
      currentSection = 'contact';
    }

    /*
     * Signal update.
     *
     * This is the important part:
     * Angular will react to this even though
     * the scroll event came from window directly.
     */
    if (this.activeSection() !== currentSection) {
      this.activeSection.set(currentSection);
    }
  }

  ngOnDestroy(): void {

    if (this.scrollHandler) {
      window.removeEventListener(
        'scroll',
        this.scrollHandler
      );
    }

    if (this.resizeHandler) {
      window.removeEventListener(
        'resize',
        this.resizeHandler
      );
    }

    if (this.animationFrameId) {
      cancelAnimationFrame(
        this.animationFrameId
      );
    }
  }

goHome(): void {
  this.activeSection.set('home');
  this.closeMenu();

  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}
}