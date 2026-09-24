import {
  AfterViewInit,
  Directive,
  ElementRef,
  OnDestroy
} from '@angular/core';

@Directive({
  selector: '[appScrollReveal]'
})
export class ScrollRevealDirective
  implements AfterViewInit, OnDestroy {

  private observer?: IntersectionObserver;

  constructor(
    private elementRef: ElementRef<HTMLElement>
  ) {}

  ngAfterViewInit(): void {

    const element =
      this.elementRef.nativeElement;

    const prefersReducedMotion =
      window.matchMedia(
        '(prefers-reduced-motion: reduce)'
      ).matches;

    if (prefersReducedMotion) {
      element.classList.add('reveal-visible');
      return;
    }

    element.classList.add('reveal-hidden');

    this.observer =
      new IntersectionObserver(
        (entries) => {

          entries.forEach((entry) => {

            if (entry.isIntersecting) {

              element.classList.remove(
                'reveal-hidden'
              );

              element.classList.add(
                'reveal-visible'
              );

              this.observer?.unobserve(element);
            }

          });

        },
        {
          threshold: 0.12,
          rootMargin: '0px 0px -40px 0px'
        }
      );

    this.observer.observe(element);
  }

  ngOnDestroy(): void {
    this.observer?.disconnect();
  }
}