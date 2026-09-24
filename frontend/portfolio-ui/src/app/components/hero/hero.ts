import {
  AfterViewInit,
  Component,
  ElementRef,
  ViewChild
} from '@angular/core';

@Component({
  selector: 'app-hero',
  imports: [],
  templateUrl: './hero.html',
  styleUrl: './hero.scss'
})
export class Hero implements AfterViewInit {

  @ViewChild('codeCard')
  codeCard!: ElementRef<HTMLElement>;


  ngAfterViewInit(): void {

    const card =
      this.codeCard.nativeElement;

    card.addEventListener(
      'mousemove',
      (event: MouseEvent) => {

        const rect =
          card.getBoundingClientRect();

        const x =
          event.clientX - rect.left;

        const y =
          event.clientY - rect.top;

        const centerX =
          rect.width / 2;

        const centerY =
          rect.height / 2;

        const rotateX =
          ((y - centerY) / centerY) * -5;

        const rotateY =
          ((x - centerX) / centerX) * 5;

        card.style.transform =
          `perspective(1000px)
           rotateX(${rotateX}deg)
           rotateY(${rotateY}deg)
           translateY(-6px)`;

        card.style.setProperty(
          '--mouse-x',
          `${x}px`
        );

        card.style.setProperty(
          '--mouse-y',
          `${y}px`
        );

      }
    );


    card.addEventListener(
      'mouseleave',
      () => {

        card.style.transform =
          `perspective(1000px)
           rotateX(0deg)
           rotateY(0deg)
           translateY(0)`;

        card.style.removeProperty(
          '--mouse-x'
        );

        card.style.removeProperty(
          '--mouse-y'
        );

      }
    );

  }

}