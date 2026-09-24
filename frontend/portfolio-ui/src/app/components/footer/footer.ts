import {
  AfterViewInit,
  Component,
  OnDestroy
} from '@angular/core';

@Component({
  selector: 'app-footer',
  imports: [],
  templateUrl: './footer.html',
  styleUrl: './footer.scss'
})
export class Footer
  implements AfterViewInit, OnDestroy {

  currentYear = new Date().getFullYear();

  private scrollHandler?: () => void;

  showBackToTop = false;

  ngAfterViewInit(): void {

    this.scrollHandler = () => {

      this.showBackToTop =
        window.scrollY > 500;

    };

    window.addEventListener(
      'scroll',
      this.scrollHandler,
      { passive: true }
    );

  }

  scrollToTop(): void {

    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });

  }

  ngOnDestroy(): void {

    if (this.scrollHandler) {

      window.removeEventListener(
        'scroll',
        this.scrollHandler
      );

    }

  }

}