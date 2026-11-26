//! Frontend-independent core foundation. Domain types belong here when M01-03 is authorized.

/// Identifies the baseline process without claiming that services are running.
pub fn baseline_message() -> &'static str {
    "ADM core foundation"
}

#[cfg(test)]
mod tests {
    #[test]
    fn baseline_message_is_stable() {
        assert_eq!(super::baseline_message(), "ADM core foundation");
    }
}
