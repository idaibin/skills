import { renderNeutralPanel } from "./neutral-panel";

if (renderNeutralPanel("neutral") !== "<section data-neutral-panel>neutral</section>") {
  throw new Error("neutral panel output changed unexpectedly");
}
