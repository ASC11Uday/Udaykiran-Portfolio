import {
  AfterViewInit,
  Component,
  ElementRef,
  OnDestroy,
  ViewChild
} from '@angular/core';

@Component({
  selector: 'app-matrix-background',
  imports: [],
  templateUrl: './matrix-background.html',
  styleUrl: './matrix-background.scss'
})
export class MatrixBackground
  implements AfterViewInit, OnDestroy {

  @ViewChild('matrixCanvas')
  canvas!: ElementRef<HTMLCanvasElement>;

  private animationFrameId = 0;
  private resizeHandler?: () => void;

  private ctx!: CanvasRenderingContext2D;

  private drops: number[] = [];
  private speeds: number[] = [];
  private lengths: number[] = [];

  private fontSize = 15;
  private columnCount = 0;

  private readonly characters =
    '01ABCDEFGHIJKLMNOPQRSTUVWXYZ{}[]<>/\\';

  ngAfterViewInit(): void {
    const canvas = this.canvas.nativeElement;
    const context = canvas.getContext('2d');

    if (!context) {
      return;
    }

    this.ctx = context;

    this.resizeCanvas();

    this.resizeHandler = () => {
      this.resizeCanvas();
    };

    window.addEventListener(
      'resize',
      this.resizeHandler,
      { passive: true }
    );

    this.animate();
  }

  private resizeCanvas(): void {
    const canvas = this.canvas.nativeElement;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    this.columnCount =
      Math.ceil(canvas.width / this.fontSize);

    this.drops = [];
    this.speeds = [];
    this.lengths = [];

    for (let i = 0; i < this.columnCount; i++) {

      /*
       * Most streams start above the viewport.
       * A few begin inside the viewport.
       */
      this.drops.push(
        Math.random() * -60
      );

      /*
       * Different speeds make the effect
       * feel less mechanical.
       */
      this.speeds.push(
        0.12 + Math.random() * 0.28
      );

      /*
       * Different trail lengths create
       * more visual depth.
       */
      this.lengths.push(
        5 + Math.floor(Math.random() * 14)
      );
    }
  }

  private animate(): void {
    const canvas = this.canvas.nativeElement;

    /*
     * Slowly fade previous frames instead
     * of completely clearing the canvas.
     */
    this.ctx.fillStyle =
      'rgba(8, 8, 8, 0.18)';

    this.ctx.fillRect(
      0,
      0,
      canvas.width,
      canvas.height
    );

    this.ctx.font =
      `${this.fontSize}px monospace`;

    for (
      let i = 0;
      i < this.columnCount;
      i++
    ) {

      const x =
        i * this.fontSize;

      const head =
        this.drops[i];

      const trailLength =
        this.lengths[i];

      /*
       * Draw the trail from darkest
       * to brightest.
       */
      for (
        let trail = trailLength;
        trail >= 0;
        trail--
      ) {

        const y =
          (head - trail) *
          this.fontSize;

        if (
          y < -this.fontSize ||
          y > canvas.height
        ) {
          continue;
        }

        const character =
          this.characters[
            Math.floor(
              Math.random() *
              this.characters.length
            )
          ];

        const intensity =
          trail === 0
            ? 0.45
            : 0.45 *
              (1 - trail / trailLength) *
              0.7;

        this.ctx.fillStyle =
          `rgba(114, 189, 125, ${intensity})`;

        this.ctx.fillText(
          character,
          x,
          y
        );
      }

      /*
       * Move the stream.
       */
      this.drops[i] +=
        this.speeds[i];

      /*
       * Restart the stream after
       * it leaves the screen.
       */
      if (
        this.drops[i] * this.fontSize >
        canvas.height +
        trailLength * this.fontSize
      ) {
        this.drops[i] =
          Math.random() * -30;
      }
    }

    this.animationFrameId =
      requestAnimationFrame(() => {
        this.animate();
      });
  }

  ngOnDestroy(): void {
    if (this.resizeHandler) {
      window.removeEventListener(
        'resize',
        this.resizeHandler
      );
    }

    cancelAnimationFrame(
      this.animationFrameId
    );
  }
}