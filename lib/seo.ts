import type { Metadata } from "next";

// Editorial targeting, not a meta-keywords tag or a claim about search volume.
export const siteOrigin = "https://tengyodalogistics.com";
type SearchCopy = { h1: string; intro: string; questions: { question: string; answer: string }[] };
export type PageSeo = {
  title: string;
  description: string;
  primary: string;
  longTail: string[];
  content: SearchCopy;
  guideSlug: string;
};

export const homeSeo = {
  title: "China Freight Forwarder | Global Sea Freight | TengYoda",
  description: "Global FCL and LCL sea freight from China across Asia, the Middle East, Europe, Africa, the Americas and Australia, with pickup and consolidation support.",
  primary: "freight forwarder in China",
  longTail: ["China freight forwarder for Oceania", "China freight forwarder for Africa", "China freight forwarder for South America", "global sea freight booking from China"],
};

export const serviceSeo: Record<string, PageSeo> = {
  "freight-forwarding": {
    title: "China Export Logistics & Freight Coordination | TengYoda",
    description: "Coordinate China export logistics with one origin-side contact: supplier pickup, warehouse handoffs, ocean or air bookings and shipment documents.",
    primary: "China export logistics",
    longTail: ["China origin freight coordination", "supplier to port logistics China", "export freight coordination from China"],
    guideSlug: "buying-from-china-checklist",
    content: { h1: "China export logistics, coordinated from origin.", intro: "China export logistics connects suppliers, domestic transport, warehouse handling and international freight bookings. TengYoda coordinates those handoffs from China so overseas importers can review one shipment plan, with clear responsibilities and a named contact.", questions: [
        { question: "Can one team coordinate supplier pickup and international shipping from China?", answer: "TengYoda can coordinate the China-side stages together or provide an individual service. Share the supplier locations, cargo-ready dates and destination so we can identify the pickup, warehouse and freight tasks to include in the quotation." },
        { question: "What should a China export logistics quotation include?", answer: "Ask for the pickup scope, origin handling, international transport and any destination services to be listed separately. Confirm the exclusions, document responsibilities and who handles each handoff before accepting the plan." },
      ] },
  },
  "sea-freight": {
    title: "Sea Freight from China: FCL & LCL Shipping | TengYoda",
    description: "Book FCL and LCL sea freight from China across Asia, the Middle East, Europe, Africa, the Americas and Australia, with origin pickup and consolidation support.",
    primary: "sea freight from China",
    longTail: ["sea freight from China to Oceania", "sea freight from China to Africa", "sea freight from China to South America", "LCL shipping from China to Australia", "FCL container shipping from China", "container shipping from China to Fremantle"],
    guideSlug: "avoid-destination-shipping-charges",
    content: { h1: "Sea freight from China: FCL and LCL shipping.", intro: "Global sea freight booking is a core TengYoda service. Our service network extends to the Middle East, Red Sea, India and Pakistan; Europe and the Mediterranean; Africa; the east and west coasts of South America; North America; Australia; and Southeast Asia. We coordinate FCL and LCL bookings, origin collection and warehouse consolidation around your cargo volume, ready date and destination.", questions: [
        { question: "Which trade lanes do you serve for sea freight from China?", answer: "Our network covers major destinations across Asia, the Middle East, Europe, Africa, the Americas and Australia. Share the destination port, cargo details and ready date for an FCL or LCL assessment. Specific sailings, carrier acceptance and destination handling are confirmed for each booking." },
        { question: "What information is needed for an FCL container shipping quote from China?", answer: "Provide the packed dimensions, gross weight, cargo-ready date, pickup location and destination port or delivery address. State the preferred container size if known. Compare ocean freight with origin and destination charges, not just the container rate." },
      ] },
  },
  "air-freight": {
    title: "Air Freight from China for Urgent Cargo | TengYoda",
    description: "Plan air freight from China for urgent shipments. Compare airport delivery scope, cargo acceptance, chargeable weight and international express options.",
    primary: "air freight from China",
    longTail: ["urgent air cargo from China", "air freight from China to Australia", "airport to airport cargo shipping China"],
    guideSlug: "express-air-lcl-fcl-guide",
    content: { h1: "Air freight from China for time-sensitive cargo.", intro: "Air freight from China can support urgent orders, replacement parts and higher-value goods when the cargo is accepted for air transport. TengYoda reviews the packed shipment and destination together, including factory collection, airport handover and any requested onward delivery.", questions: [
        { question: "How do I request an air freight quote from China to Australia?", answer: "Provide the product description, package count, external dimensions, gross weight, ready date and destination airport or postcode. Identify batteries, liquids or other special contents before booking. The quotation should distinguish airport charges from any final-delivery services." },
        { question: "Should urgent cargo from China travel by air freight or express?", answer: "Compare both using the same packed cargo and delivery scope. Express may suit smaller parcels, while air freight may offer another option for larger time-sensitive shipments. Acceptance, handling, chargeable weight and the complete delivery plan determine the appropriate choice." },
      ] },
  },
  "international-express": {
    title: "Express Shipping from China: DHL, FedEx & UPS | TengYoda",
    description: "Compare DHL, FedEx and UPS express shipping from China for samples and parcels. Request a quote using packed dimensions, weight and destination postcode.",
    primary: "express shipping from China",
    longTail: ["DHL shipping from China", "FedEx parcel shipping from China", "UPS express from China", "send product samples from China overseas"],
    guideSlug: "express-air-lcl-fcl-guide",
    content: { h1: "Express shipping from China with DHL, FedEx and UPS options.", intro: "Request international courier options for product samples, parcels and smaller orders collected in China. TengYoda compares DHL, FedEx and UPS services against the actual shipment profile; service availability and acceptance are confirmed before dispatch.", questions: [
        { question: "Can I send product samples from China by DHL, FedEx or UPS?", answer: "Send the sample description, supplier address, packed sizes, weight and receiver postcode for review. Tell us about batteries, liquids or other special characteristics. A service option can be confirmed only after the cargo and destination are checked." },
        { question: "How can I compare international courier quotes from China?", answer: "Use identical package measurements and destination details. Check the chargeable weight, pickup scope, handling or delivery surcharges and destination responsibilities. A parcel transport rate should not be assumed to include every import cost." },
      ] },
  },
  "china-import-export": {
    title: "China Procurement & Sourcing Support | TengYoda Logistics",
    description: "China procurement support for overseas buyers: supplier coordination, order follow-up, export preparation and consolidated shipping through TengYoda.",
    primary: "China procurement services",
    longTail: ["China sourcing and shipping support", "Foshan procurement and export coordination", "buying from multiple suppliers in China"],
    guideSlug: "buying-from-china-checklist",
    content: { h1: "China procurement and sourcing support for overseas buyers.", intro: "Connect China procurement with the shipment plan from the start. From our Foshan operations base, TengYoda supports supplier coordination, order follow-up and export preparation, with warehouse consolidation available for purchases from multiple suppliers.", questions: [
        { question: "Can you coordinate China sourcing and shipping in one plan?", answer: "Share your product specifications, supplier information, quantities and destination. We can review the purchasing coordination and transport tasks together. For furniture, lighting or building-material orders, provide packing information early so transport planning reflects the actual shipment." },
        { question: "What should I confirm before buying from multiple suppliers in China?", answer: "Confirm the specification, quantity, order reference and cargo-ready date with each supplier. Agree on receiving marks and checking requirements before dispatching orders to a shared warehouse. Keep the purchasing responsibilities and logistics scope clear in writing." },
      ] },
  },
  "transport-warehousing": {
    title: "China Domestic Trucking & Factory Pickup | TengYoda",
    description: "Arrange domestic trucking in China, factory pickup and warehouse delivery. Coordinate cargo collection with export warehouse, port and airport handoffs.",
    primary: "China domestic trucking",
    longTail: ["factory pickup service in China", "factory to warehouse transport China", "China warehouse to port transport"],
    guideSlug: "buying-from-china-checklist",
    content: { h1: "China domestic trucking and factory pickup.", intro: "Move export cargo between Chinese factories, receiving warehouses, ports and airports. TengYoda coordinates domestic road transport with the receiving window and international booking plan, using the actual cargo size, loading conditions and collection address.", questions: [
        { question: "Can you collect goods from a Chinese factory and deliver to a warehouse?", answer: "Provide both addresses, supplier contacts, package details and the date the goods can be loaded. We can assess factory-to-warehouse transport and coordinate receiving instructions with the relevant warehouse before the truck is booked." },
        { question: "What affects the scope of a domestic trucking quote in China?", answer: "Pickup distance, vehicle requirements, cargo weight and dimensions, loading access and delivery timing all matter. Explain who provides loading and unloading equipment and whether an appointment is needed at the warehouse, port or airport." },
      ] },
  },
  "cargo-consolidation": {
    title: "Cargo Consolidation in China: Multiple Suppliers | TengYoda",
    description: "Combine orders from multiple Chinese suppliers with warehouse consolidation in Qingdao, Yiwu or Shenzhen. Plan receiving, checks and one export shipment.",
    primary: "cargo consolidation in China",
    longTail: ["combine shipments from multiple suppliers in China", "China warehouse consolidation services", "Yiwu consolidation warehouse", "Shenzhen cargo consolidation"],
    guideSlug: "express-air-lcl-fcl-guide",
    content: { h1: "Cargo consolidation in China for multiple suppliers.", intro: "Combine supplier orders before international dispatch with TengYoda's China warehouse consolidation support. Receiving locations in Qingdao, Yiwu and Shenzhen help connect separate orders to one outbound plan. Confirm the receiving warehouse and order references before suppliers send goods.", questions: [
        { question: "How can I combine shipments from multiple suppliers in China?", answer: "Prepare a supplier list with order references, expected arrival dates and package details. Agree the receiving instructions and checking scope first. Once the required goods arrive, compare the combined shipment with an air, LCL or FCL plan based on final measurements." },
        { question: "Should I use a Yiwu or Shenzhen consolidation warehouse?", answer: "Choose the receiving location around supplier addresses, cargo-ready dates and the export route, rather than the city name alone. TengYoda can review Qingdao, Yiwu and Shenzhen receiving options. Confirm the location, appointment and shipping marks with Vinson before delivery." },
      ] },
  },
  "oversize-freight": {
    title: "Oversized Cargo & Heavy Machinery Shipping China | TengYoda",
    description: "Plan oversized cargo shipping from China with a review of dimensions, lifting points, loading access, equipment needs and heavy machinery transport options.",
    primary: "oversized cargo shipping from China",
    longTail: ["heavy machinery shipping from China", "shipping excavators from China", "oversized equipment transport China"],
    guideSlug: "buying-from-china-checklist",
    content: { h1: "Oversized cargo and heavy machinery shipping from China.", intro: "Prepare machinery and non-standard cargo for China-origin transport with an equipment and route review. TengYoda coordinates the pickup and export plan around each piece's transport dimensions, weight, lifting points and handling limits.", questions: [
        { question: "What is needed to plan heavy machinery shipping from China?", answer: "Provide the model, transport dimensions, weight, photographs, lifting points and loading facilities. For excavators or mobile equipment, state whether the unit can move under its own power and identify any parts that can be removed for transport." },
        { question: "Does oversized equipment always require a special container?", answer: "The appropriate method depends on the cargo and available equipment. A review may consider standard or special equipment, RoRo or breakbulk options. Confirm route feasibility, securing arrangements and carrier acceptance before booking." },
      ] },
  },
  "roro-project-cargo": {
    title: "RoRo Shipping & Project Cargo from China | TengYoda",
    description: "Coordinate RoRo shipping and project cargo from China for vehicles and mobile equipment. Review cargo condition, route options and carrier acceptance.",
    primary: "RoRo shipping from China",
    longTail: ["vehicle shipping from China", "project cargo logistics China", "breakbulk cargo shipping from China"],
    guideSlug: "avoid-destination-shipping-charges",
    content: { h1: "RoRo shipping and project cargo logistics from China.", intro: "Coordinate vehicle, mobile-equipment and project cargo shipments from China through a route-specific transport plan. TengYoda reviews the cargo condition, port handoffs and carrier acceptance before recommending a RoRo or alternative shipping arrangement.", questions: [
        { question: "Can vehicles and mobile machinery be shipped from China by RoRo?", answer: "RoRo can be considered where the cargo condition, handling method and available vessel service are suitable. Provide the dimensions, weight, operational condition and destination. Confirm the carrier's requirements for the particular unit before committing to shipment." },
        { question: "How do you plan project cargo or breakbulk shipping from China?", answer: "Start with a piece-by-piece cargo list, drawings, lifting information and the required destination handoffs. Each stage needs compatible loading, transport and receiving arrangements. TengYoda coordinates the China-side plan and clarifies any partner-managed destination scope." },
      ] },
  },
};

export const blogSeo: Record<string, { title: string; description: string; primary: string; longTail: string[]; serviceSlugs: string[] }> = {
  "shipping-excavator-china-costa-rica": { title: "Ship an Excavator China to Costa Rica: RoRo vs FR", description: "Compare RoRo, breakbulk and flat-rack shipping for a 30–35 ton excavator from China to Costa Rica, including quote details, ports and risk controls.", primary: "shipping excavator from China to Costa Rica", longTail: ["RoRo shipping excavator China to Costa Rica", "breakbulk excavator Tianjin to Caldera", "flat rack excavator shipping China", "heavy machinery shipping to Costa Rica"], serviceSlugs: ["roro-project-cargo", "oversize-freight", "freight-forwarding"] },
  "shipping-marks-for-china-consolidation": { title: "Shipping Marks for China Consolidation: Carton Guide", description: "Learn when every carton needs a shipping mark, what details to include and how marks prevent lost or mixed cargo during China warehouse consolidation.", primary: "shipping marks for cartons from China", longTail: ["do I need shipping marks on every carton", "shipping mark requirements for China consolidation", "carton labels for multiple suppliers in China", "what to include on a shipping mark"], serviceSlugs: ["cargo-consolidation", "transport-warehousing", "freight-forwarding"] },
  "can-my-product-be-exported-from-china": { title: "Can My Product Be Exported from China? Checklist", description: "Check whether a product can be exported from China, which cargo needs special documents and what importers should confirm before pickup or booking.", primary: "can my product be exported from China", longTail: ["restricted cargo shipping from China", "what products cannot be exported from China", "documents for special cargo export from China", "can batteries liquids powder be shipped from China"], serviceSlugs: ["freight-forwarding", "air-freight", "sea-freight"] },
  "door-to-door-shipping-from-china-inclusions": { title: "Door-to-Door Shipping from China: What Is Included?", description: "Learn what door-to-door shipping from China includes, which charges may be excluded and how small importers can compare complete delivery quotes.", primary: "door-to-door shipping from China", longTail: ["what is included in door to door shipping from China", "door to door freight quote China", "does door to door shipping include customs clearance", "hidden charges door to door shipping China"], serviceSlugs: ["freight-forwarding", "sea-freight", "transport-warehousing"] },
  "exw-vs-fob-from-china-small-importers": { title: "EXW vs FOB from China: Small Importer Guide", description: "Compare EXW and FOB shipping from China: pickup, export clearance, origin charges, buyer control and the true cost for small importers.", primary: "EXW vs FOB from China", longTail: ["EXW or FOB which is better for small importers", "EXW shipping from China costs", "FOB shipping from China responsibilities", "difference between EXW and FOB China"], serviceSlugs: ["freight-forwarding", "transport-warehousing", "cargo-consolidation"] },
  "why-freight-quote-changed-after-pickup": { title: "Why Did My Freight Quote Change After Pickup?", description: "Learn eight reasons a freight quote changes after pickup, which adjustments are reasonable and how to prevent unexpected shipping costs from China.", primary: "why freight quote changed after pickup", longTail: ["freight quote different from final invoice", "shipping cost increased after pickup", "LCL quote changed after warehouse measurement", "unexpected freight charges from China"], serviceSlugs: ["freight-forwarding", "transport-warehousing", "cargo-consolidation"] },
  "how-to-choose-reliable-china-freight-forwarder": { title: "Reliable Freight Forwarder in China: 10-Point Checklist", description: "Learn how to verify a China freight forwarder, compare quotation scope and reduce cargo, payment, destination-charge and communication risks.", primary: "reliable freight forwarder in China", longTail: ["how to choose a freight forwarder in China", "verify China freight forwarder", "China shipping agent checklist", "compare freight quotes from China"], serviceSlugs: ["freight-forwarding", "sea-freight", "transport-warehousing"] },
  "shipping-500-cars-china-to-oman-roro-vs-container": { title: "Shipping 500 Cars from China to Oman: RoRo vs 40HQ", description: "Compare RoRo and four-car 40HQ container plans for shipping 500 sedans from China to Oman, including cost, loading, unloading and risk controls.", primary: "shipping cars from China to Oman", longTail: ["Nansha to Duqm vehicle shipping", "RoRo shipping China to Oman", "four cars in one 40HQ container", "COC vs SOC container for vehicles"], serviceSlugs: ["roro-project-cargo", "sea-freight", "freight-forwarding"] },
  "australia-import-container-release-bill-of-lading-guide": { title: "Australia Container Release & Bill of Lading Guide", description: "Understand container numbers, bills of lading, carrier invoices, customs clearance, cargo release, free time and empty returns for Australian imports.", primary: "Australia container release process", longTail: ["bill of lading Australia import", "shipping line destination charges Australia", "empty container return free time Australia", "why shipping line has not released bill of lading"], serviceSlugs: ["freight-forwarding", "sea-freight", "transport-warehousing"] },
  "australia-import-process-after-china-customs-release": { title: "After China Customs Release: Australia Import Process", description: "Understand the China-to-Australia import process after customs release: terminal gate-in, vessel loading, documents, Australian clearance and delivery.", primary: "importing from China to Australia process", longTail: ["what happens after China customs release", "China customs clearance to Australia", "Australia import process from China", "first time importing from China to Australia"], serviceSlugs: ["freight-forwarding", "sea-freight", "transport-warehousing"] },
  "buying-from-china-checklist": { title: "Buying from China: First-Time Importer Checklist | TengYoda", description: "A practical checklist for first-time importers buying from China: supplier orders, packing details, cargo-ready dates, documents and shipping quotations.", primary: "buying from China checklist", longTail: ["what to check before buying from China", "first time importing from China", "supplier packing checklist for export"], serviceSlugs: ["china-import-export", "cargo-consolidation", "transport-warehousing"] },
  "express-air-lcl-fcl-guide": { title: "Shipping from China: Express vs Air vs LCL vs FCL | TengYoda", description: "Compare express, air freight, LCL and FCL shipping from China using the same cargo, urgency, handling needs and complete delivery-cost scope.", primary: "express vs air freight vs LCL vs FCL", longTail: ["how to choose shipping method from China", "LCL vs FCL shipping from China", "air freight vs express shipping China"], serviceSlugs: ["international-express", "air-freight", "sea-freight"] },
  "avoid-destination-shipping-charges": { title: "Destination Shipping Charges: 5 Importer Checks | TengYoda", description: "Check destination shipping charges, release responsibilities, delivery access and container return arrangements before your China-origin cargo arrives.", primary: "destination shipping charges", longTail: ["how to avoid unexpected destination charges", "China import shipment destination fees", "container delivery and return planning"], serviceSlugs: ["sea-freight", "freight-forwarding", "roro-project-cargo"] },
};

export function pageMetadata(title: string, description: string, path: string): Metadata {
  return { title, description, alternates: { canonical: `${siteOrigin}${path}` } };
}
