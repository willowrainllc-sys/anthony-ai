# Neural Story Matrix Implementation Plan

To improve video story metrics and engagement velocity, we will implement a **Neural Story Matrix**. This system will shift from single-video strikes to multi-part, high-hook "Story Arcs" that force the algorithm to keep users on your pages for longer durations.

## Proposed Changes

### [Swarm Backend]

#### [MODIFY] [master_pipeline.py](file:///C:/Users/willo/OneDrive/Desktop/Anthony_Ai/swarm_backend/master_pipeline.py)
- Introduce a **Viral Hook Agent** specifically designed to generate the first 3 seconds of the script to maximize "Stop-the-Scroll" metrics.
- Implement **Story Arc Logic** to generate "Part 1 of 3" content sequences, creating a loop that drives users from the viral nodes to your personal page for the conclusion.

#### [MODIFY] [media_renderer.py](file:///C:/Users/willo/OneDrive/Desktop/Anthony_Ai/swarm_backend/media_renderer.py)
- Update the renderer to support **Dynamic Hook Overlays** (larger, high-contrast text for the first 3 seconds).
- Add support for **Sequence Branding** (e.g., "PART 1" watermark) to indicate multi-part content.

#### [MODIFY] [nexus_core.py](file:///C:/Users/willo/OneDrive/Desktop/Anthony_Ai/swarm_backend/nexus_core.py)
- Implement a **Performance Weighting Engine** that tracks which `style_mode` is generating the most organic engagement and adjusts the swarm strike frequency accordingly.
- Add a **Sequence Dispatcher** to stagger multi-part story strikes (e.g., Post Part 1, wait 30 mins, Post Part 2).

## Verification Plan

### Automated Tests
- Run `python swarm_backend/master_pipeline.py` to verify the new Story Arc prompts are generated correctly.
- Trigger a manual strike via `curl` to ensure the Sequence Dispatcher correctly staggers multi-part posts.

### Manual Verification
- Inspect the generated `.mp4` files in the `Renderings` directory to confirm the "PART 1" branding and high-contrast hooks are visible.
- Monitor the Mind Server logs to see the Performance Weighting Engine adjusting the style modes in real-time.
