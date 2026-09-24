import {
  AfterViewInit,
  Component,
  ElementRef,
  HostBinding,
  OnDestroy,
  Renderer2,
  inject
} from '@angular/core';

@Component({
  selector: 'app-custom-cursor',
  imports: [],
  templateUrl: './custom-cursor.html',
  styleUrl: './custom-cursor.scss'
})
export class CustomCursor
  implements AfterViewInit, OnDestroy {

  private renderer = inject(Renderer2);

  private elementRef =
    inject(ElementRef);

  private dot!: HTMLElement;

  private ring!: HTMLElement;

  private mouseX = 0;

  private mouseY = 0;

  private ringX = 0;

  private ringY = 0;

  private animationFrameId = 0;

  private cleanupFunctions: (() => void)[] = [];


  @HostBinding('class.interactive')
  isInteractive = false;


  @HostBinding('class.magnetic')
  isMagnetic = false;


  ngAfterViewInit(): void {

    this.dot =
      this.elementRef.nativeElement
        .querySelector('.cursor-dot');

    this.ring =
      this.elementRef.nativeElement
        .querySelector('.cursor-ring');


    this.setupMouseTracking();

    this.setupInteractiveElements();

    this.animate();

  }


  private setupMouseTracking(): void {

    const cleanup =
      this.renderer.listen(
        'document',
        'mousemove',
        (event: MouseEvent) => {

          this.mouseX =
            event.clientX;

          this.mouseY =
            event.clientY;


          this.dot.style.transform =
            `translate(
              ${this.mouseX}px,
              ${this.mouseY}px
            ) translate(-50%, -50%)`;

        }
      );


    this.cleanupFunctions.push(
      cleanup
    );

  }


  private setupInteractiveElements(): void {

    const interactiveElements =
      document.querySelectorAll(
        'a, button, input, textarea'
      );


    interactiveElements.forEach(
      (element) => {

        const enterCleanup =
          this.renderer.listen(
            element,
            'mouseenter',
            () => {

              this.isInteractive =
                true;

            }
          );


        const leaveCleanup =
          this.renderer.listen(
            element,
            'mouseleave',
            () => {

              this.isInteractive =
                false;

              this.isMagnetic =
                false;

            }
          );


        this.cleanupFunctions.push(
          enterCleanup,
          leaveCleanup
        );


        /*
         * Magnetic effect only for buttons
         * and important links.
         */
        if (
          element.tagName === 'BUTTON' ||
          element.classList.contains(
            'primary-button'
          ) ||
          element.classList.contains(
            'secondary-button'
          ) ||
          element.classList.contains(
            'submit-button'
          )
        ) {

          const moveCleanup =
            this.renderer.listen(
              element,
              'mousemove',
              (event: MouseEvent) => {

                this.handleMagneticMove(
                  event,
                  element as HTMLElement
                );

              }
            );


          const leaveMagneticCleanup =
            this.renderer.listen(
              element,
              'mouseleave',
              () => {

                this.resetMagnetic(
                  element as HTMLElement
                );

              }
            );


          this.cleanupFunctions.push(
            moveCleanup,
            leaveMagneticCleanup
          );

        }

      }
    );

  }


  private handleMagneticMove(
    event: MouseEvent,
    element: HTMLElement
  ): void {

    const rect =
      element.getBoundingClientRect();


    const centerX =
      rect.left +
      rect.width / 2;

    const centerY =
      rect.top +
      rect.height / 2;


    const offsetX =
      (event.clientX - centerX) *
      0.15;

    const offsetY =
      (event.clientY - centerY) *
      0.15;


    this.isMagnetic =
      true;


    element.style.transform =
      `translate(
        ${offsetX}px,
        ${offsetY}px
      )`;

  }


  private resetMagnetic(
    element: HTMLElement
  ): void {

    element.style.transform =
      '';

    this.isMagnetic =
      false;

  }


  private animate(): void {

    /*
     * Ring follows the cursor with
     * a small amount of lag.
     */
    this.ringX +=
      (this.mouseX - this.ringX) *
      0.16;

    this.ringY +=
      (this.mouseY - this.ringY) *
      0.16;


    this.ring.style.transform =
      `translate(
        ${this.ringX}px,
        ${this.ringY}px
      ) translate(-50%, -50%)`;


    this.animationFrameId =
      requestAnimationFrame(
        () => this.animate()
      );

  }


  ngOnDestroy(): void {

    cancelAnimationFrame(
      this.animationFrameId
    );


    this.cleanupFunctions.forEach(
      (cleanup) => cleanup()
    );

  }

}