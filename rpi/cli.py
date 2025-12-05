"""
Standalone command-line interface for Raspberry Pi
Simple script to run grading from terminal
"""

import argparse
import sys
import json
from pathlib import Path

from pipeline import RPiPipeline
from camera import RPiCameraCapture, detect_available_cameras


def main():
    """Main entry point for RPi CLI"""
    parser = argparse.ArgumentParser(
        description='Raspberry Pi Answer Sheet Checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Grade with image file
  python rpi_cli.py --image answer.jpg --answers "Q1" "Q2" "Q3"
  
  # Capture from camera and grade
  python rpi_cli.py --camera 0 --answers "Answer1" "Answer2"
  
  # Show available cameras
  python rpi_cli.py --list-cameras
  
  # Load answers from file
  python rpi_cli.py --image answer.jpg --answer-file answers.json
        """
    )
    
    # Image source
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--image', type=str,
                            help='Path to answer sheet image')
    input_group.add_argument('--camera', type=int,
                            help='Camera device ID (0 for default)')
    input_group.add_argument('--list-cameras', action='store_true',
                            help='List available cameras')
    
    # Answer key
    answer_group = parser.add_mutually_exclusive_group()
    answer_group.add_argument('--answers', nargs='+',
                             help='Answer key (space-separated)')
    answer_group.add_argument('--answer-file', type=str,
                             help='JSON file with answer key')
    
    # Options
    parser.add_argument('--threshold', type=float, default=0.70,
                       help='Grading threshold (0.0-1.0, default: 0.70)')
    parser.add_argument('--output', type=str,
                       help='Save results to JSON file')
    parser.add_argument('--preview', type=int, default=0,
                       help='Show camera preview for N seconds')
    parser.add_argument('--quiet', action='store_true',
                       help='Minimal output')
    
    args = parser.parse_args()
    
    # Handle list cameras
    if args.list_cameras:
        cameras = detect_available_cameras()
        if cameras:
            print("📷 Available cameras:")
            for cam_id in cameras:
                print(f"   Camera {cam_id}")
        else:
            print("❌ No cameras found")
        return
    
    # Load answer key
    answer_key = None
    
    if args.answer_file:
        try:
            with open(args.answer_file, 'r') as f:
                data = json.load(f)
                answer_key = data if isinstance(data, list) else data.get('answers', [])
            print(f"✓ Loaded {len(answer_key)} answers from {args.answer_file}")
        except Exception as e:
            print(f"❌ Failed to load answer file: {e}")
            sys.exit(1)
    
    elif args.answers:
        answer_key = args.answers
        print(f"✓ Answer key: {len(answer_key)} questions")
    
    else:
        print("❌ No answer key provided")
        sys.exit(1)
    
    # Initialize pipeline
    pipeline = RPiPipeline(threshold=args.threshold)
    
    try:
        # Handle camera input
        if args.camera is not None:
            print(f"📷 Initializing camera {args.camera}...")
            camera = RPiCameraCapture(camera_id=args.camera)
            
            if args.preview:
                frame = camera.capture_preview(duration_sec=args.preview)
            else:
                frame = camera.capture()
            
            if frame is None:
                print("❌ Failed to capture from camera")
                sys.exit(1)
            
            # Save temporary image
            temp_image = Path("/tmp/rpi_capture.jpg")
            import cv2
            cv2.imwrite(str(temp_image), frame)
            image_path = str(temp_image)
            camera.release()
            print(f"✓ Captured image: {image_path}")
        
        else:
            image_path = args.image
        
        # Run pipeline
        results = pipeline.full_pipeline(image_path, answer_key, 
                                        save_output=args.output)
        
        # Print results
        if not args.quiet:
            print("\n" + "="*60)
            print("📋 RESULTS")
            print("="*60)
            
            for q_num, result in results.items():
                if q_num == "summary":
                    continue
                
                if isinstance(result, dict) and "status" in result:
                    print(f"\nQ{q_num}: {result['status']}")
                    print(f"Similarity: {result['similarity']*100:.1f}%")
                    print(f"Expected: {result['expected'][:50]}")
                    print(f"Got:      {result['student'][:50]}")
            
            if "summary" in results:
                summary = results["summary"]
                print("\n" + "-"*60)
                print(f"✓ Final Score: {summary['percentage']:.1f}%")
                print(f"  Passed: {summary['passed']}/{summary['total_questions']}")
        
        sys.exit(0)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
