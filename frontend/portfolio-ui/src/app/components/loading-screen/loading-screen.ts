import {
  AfterViewInit,
  Component,
  ElementRef,
  EventEmitter,
  OnDestroy,
  Output,
  ViewChild
} from '@angular/core';

interface MatrixColumn {
  x: number;
  y: number;
  speed: number;
  length: number;
  opacity: number;
}

@Component({
  selector: 'app-loading-screen',
  imports: [],
  templateUrl: './loading-screen.html',
  styleUrl: './loading-screen.scss'
})
export class LoadingScreen
  implements AfterViewInit, OnDestroy {

  @ViewChild('matrixCanvas', { static: true })
  canvas!: ElementRef<HTMLCanvasElement>;

  @Output()
  loadingComplete = new EventEmitter<void>();

  private ctx!: CanvasRenderingContext2D;

  private animationFrameId = 0;

  private timeoutId?: ReturnType<typeof setTimeout>;

  private resizeHandler = () => {
    this.setupCanvas();
  };

  private columns: MatrixColumn[] = [];

  private lastFrameTime = 0;

  private readonly fontSize = 18;

  /*
   * Matrix-style character set.
   */
  private readonly characters =
    'アカサタナハマヤラワ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';


  ngAfterViewInit(): void {

    this.setupCanvas();

    window.addEventListener(
      'resize',
      this.resizeHandler
    );

    this.lastFrameTime =
      performance.now();

    this.animate(
      this.lastFrameTime
    );


    /*
     * Keep the Matrix animation visible
     * for around 2.5 seconds.
     */
    this.timeoutId = setTimeout(() => {

      const screen =
        this.canvas.nativeElement.parentElement;

      screen?.classList.add('is-exiting');

      setTimeout(() => {

        this.loadingComplete.emit();

      }, 800);

    }, 2500);
  }


  private setupCanvas(): void {

    const canvas =
      this.canvas.nativeElement;

    const dpr =
      window.devicePixelRatio || 1;

    canvas.width =
      window.innerWidth * dpr;

    canvas.height =
      window.innerHeight * dpr;

    canvas.style.width =
      `${window.innerWidth}px`;

    canvas.style.height =
      `${window.innerHeight}px`;

    this.ctx =
      canvas.getContext('2d')!;

    this.ctx.setTransform(
      dpr,
      0,
      0,
      dpr,
      0,
      0
    );

    this.createColumns();
  }


  private createColumns(): void {

    const width =
      window.innerWidth;

    const height =
      window.innerHeight;


    /*
     * Smaller spacing gives us more streams
     * distributed across the entire screen.
     *
     * Example:
     * 1920 / 28 ≈ 68 possible positions
     */
    const columnSpacing = 30;

    const totalColumns =
      Math.ceil(
        width / columnSpacing
      );


    this.columns = [];


    for (
      let i = 0;
      i < totalColumns;
      i++
    ) {

      /*
       * Not every possible position gets a stream.
       * This keeps the Matrix effect organic.
       */
      const shouldCreate =
        Math.random() > 0.25;


      if (!shouldCreate) {
        continue;
      }


      /*
       * Keep streams aligned to a loose grid,
       * while adding a little randomness.
       */
      const x =
        i * columnSpacing +
        (Math.random() * 8 - 4);


      /*
       * Start streams throughout the screen,
       * not only from above the screen.
       *
       * This makes the loading screen immediately
       * populated when it appears.
       */
      const y =
        Math.random() *
        height *
        1.1;


      /*
       * Long streams similar to the reference.
       */
      const length =
        Math.floor(
          25 +
          Math.random() * 55
        );


      /*
       * Pixels per second.
       *
       * This is intentionally much faster.
       */
      const speed =
        220 +
        Math.random() * 220;


      /*
       * Keep most streams dark.
       */
      const opacity =
        0.12 +
        Math.random() * 0.20;


      this.columns.push({
        x,
        y,
        speed,
        length,
        opacity
      });

    }

  }


  private animate(
    currentTime: number
  ): void {

    const width =
      window.innerWidth;

    const height =
      window.innerHeight;


    /*
     * Calculate real elapsed time.
     *
     * This makes the Matrix speed consistent
     * on 60Hz, 120Hz, 144Hz, etc.
     */
    const deltaTime =
      Math.min(
        currentTime -
        this.lastFrameTime,
        50
      );


    this.lastFrameTime =
      currentTime;


    /*
     * Convert milliseconds to seconds.
     */
    const deltaSeconds =
      deltaTime / 1000;


    /*
     * Fade previous frames.
     *
     * This creates the trailing effect.
     */
    this.ctx.fillStyle =
      'rgba(0, 0, 0, 0.18)';

    this.ctx.fillRect(
      0,
      0,
      width,
      height
    );


    this.ctx.font =
      `${this.fontSize}px monospace`;

    this.ctx.textAlign =
      'center';


    for (
      const column of this.columns
    ) {

      /*
       * Draw the stream.
       */
      for (
        let i = 0;
        i < column.length;
        i++
      ) {

        const y =
          column.y -
          i * this.fontSize;


        /*
         * Skip characters outside
         * the visible screen.
         */
        if (
          y < -this.fontSize ||
          y > height +
          this.fontSize
        ) {
          continue;
        }


        const character =
          this.getRandomCharacter();


        /*
         * 0 = head
         * 1 = end of trail
         */
        const position =
          i / column.length;


        /*
         * Fade toward the end of the trail.
         */
        let alpha =
          column.opacity *
          (1 - position) *
          (0.65 + Math.random() * 0.35);


        /*
         * Make the last portion
         * significantly darker.
         */
        if (position > 0.65) {

          alpha *= 0.45;

        }


        /*
         * Occasionally make the head
         * noticeably brighter.
         */
        const isBright =
          i === 0 &&
          Math.random() > 0.45;


        if (isBright) {

          this.ctx.fillStyle =
            `rgba(
      90,
215,
105,
      ${Math.min(
              alpha * 1.8,
              0.55
            )}
    )`;

        } else {

          this.ctx.fillStyle =
            `rgba(
    0,
    175,
    50,
    ${alpha}
  )`;

        }


        this.ctx.fillText(
          character,
          column.x,
          y
        );

      }


      /*
       * Move the stream.
       *
       * Because speed is pixels/second,
       * this is refresh-rate independent.
       */
      column.y +=
        column.speed *
        deltaSeconds;


      /*
       * When the whole stream leaves
       * the bottom, restart it above.
       */
      if (
        column.y -
        column.length *
        this.fontSize >
        height
      ) {

        column.y =
          -Math.random() *
          height *
          0.6;


        column.speed =
          220 +
          Math.random() * 220;


        column.length =
          Math.floor(
            25 +
            Math.random() * 55
          );


        column.opacity =
          0.22 +
          Math.random() * 0.30;

      }

    }


    this.animationFrameId =
      requestAnimationFrame(
        (time) =>
          this.animate(time)
      );
  }


  private getRandomCharacter(): string {

    return this.characters[
      Math.floor(
        Math.random() *
        this.characters.length
      )
    ];

  }


  ngOnDestroy(): void {

    cancelAnimationFrame(
      this.animationFrameId
    );


    window.removeEventListener(
      'resize',
      this.resizeHandler
    );


    if (this.timeoutId) {

      clearTimeout(
        this.timeoutId
      );

    }

  }

}